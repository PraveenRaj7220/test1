import fitz  # PyMuPDF
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Union
import json
from paddleocr import PaddleOCR
import logging
from concurrent.futures import ThreadPoolExecutor
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InvoiceExtractor:
    def __init__(self, use_gpu: bool = False):
        """
        Initialize the invoice extractor.
        
        Args:
            use_gpu (bool): Whether to use GPU for OCR processing
        """
        self.ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=use_gpu)
        self.parallel = joblib.Parallel(n_jobs=-1)
        
    def process_pdf(self, pdf_path: Union[str, Path]) -> Dict:
        """
        Process a single PDF file and extract invoice information.
        
        Args:
            pdf_path (Union[str, Path]): Path to the PDF file
            
        Returns:
            Dict: Extracted invoice information
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        try:
            # Extract text using PyMuPDF
            doc = fitz.open(str(pdf_path))
            text_content = self._extract_text(doc)
            
            # Perform OCR if needed
            if self._needs_ocr(text_content):
                logger.info("Performing OCR on the document")
                ocr_results = self._perform_ocr(pdf_path)
                text_content = self._combine_text(text_content, ocr_results)
            
            # Extract structured data
            invoice_data = self._extract_structured_data(text_content)
            
            return invoice_data
            
        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {str(e)}")
            raise
            
    def process_batch(self, input_dir: Union[str, Path], output_dir: Union[str, Path]) -> None:
        """
        Process multiple PDF files in a directory.
        
        Args:
            input_dir (Union[str, Path]): Directory containing PDF files
            output_dir (Union[str, Path]): Directory to save results
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        pdf_files = list(input_dir.glob("*.pdf"))
        
        def process_single(pdf_path):
            try:
                result = self.process_pdf(pdf_path)
                output_path = output_dir / f"{pdf_path.stem}.json"
                with open(output_path, "w") as f:
                    json.dump(result, f, indent=2)
                return True
            except Exception as e:
                logger.error(f"Failed to process {pdf_path}: {str(e)}")
                return False
                
        results = self.parallel(joblib.delayed(process_single)(pdf) for pdf in pdf_files)
        success_rate = sum(results) / len(results)
        logger.info(f"Batch processing complete. Success rate: {success_rate:.2%}")
        
    def _extract_text(self, doc: fitz.Document) -> str:
        """Extract text from PDF using PyMuPDF."""
        text = ""
        for page in doc:
            text += page.get_text()
        return text
        
    def _needs_ocr(self, text: str) -> bool:
        """Determine if OCR is needed based on text content."""
        # Simple heuristic: if the text is too short or contains mostly whitespace
        return len(text.strip()) < 100
        
    def _perform_ocr(self, pdf_path: Path) -> List[str]:
        """Perform OCR on the PDF using PaddleOCR."""
        result = self.ocr.ocr(str(pdf_path))
        return [line[1][0] for page in result for line in page]
        
    def _combine_text(self, pdf_text: str, ocr_text: List[str]) -> str:
        """Combine PDF text and OCR results."""
        return pdf_text + "\n" + "\n".join(ocr_text)
        
    def _extract_structured_data(self, text: str) -> Dict:
        """Extract structured data from text using regex and layout analysis."""
        # This is a placeholder for the actual extraction logic
        # In a real implementation, this would use regex patterns and ML models
        # to identify and extract specific fields
        
        # Example structure
        return {
            "invoice_number": self._extract_invoice_number(text),
            "date": self._extract_date(text),
            "total_amount": self._extract_total_amount(text),
            "vendor_name": self._extract_vendor_name(text),
            "line_items": self._extract_line_items(text)
        }
        
    def _extract_invoice_number(self, text: str) -> Optional[str]:
        """Extract invoice number from text."""
        # Placeholder implementation
        return None
        
    def _extract_date(self, text: str) -> Optional[str]:
        """Extract date from text."""
        # Placeholder implementation
        return None
        
    def _extract_total_amount(self, text: str) -> Optional[float]:
        """Extract total amount from text."""
        # Placeholder implementation
        return None
        
    def _extract_vendor_name(self, text: str) -> Optional[str]:
        """Extract vendor name from text."""
        # Placeholder implementation
        return None
        
    def _extract_line_items(self, text: str) -> List[Dict]:
        """Extract line items from text."""
        # Placeholder implementation
        return [] 