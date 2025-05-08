import pytest
from pathlib import Path
from invoice_extractor.extractor import InvoiceExtractor
import tempfile
import json

@pytest.fixture
def extractor():
    return InvoiceExtractor(use_gpu=False)

def test_process_pdf_nonexistent(extractor):
    with pytest.raises(FileNotFoundError):
        extractor.process_pdf("nonexistent.pdf")

def test_process_pdf_empty(extractor):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        with pytest.raises(Exception):
            extractor.process_pdf(tmp.name)

def test_batch_processing(extractor, tmp_path):
    # Create test directories
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    
    # Create empty PDF files
    for i in range(3):
        (input_dir / f"test_{i}.pdf").touch()
    
    # Run batch processing
    extractor.process_batch(input_dir, output_dir)
    
    # Check if output files were created
    assert len(list(output_dir.glob("*.json"))) == 3

def test_extract_text(extractor):
    # This is a placeholder test
    # In a real implementation, you would test with actual PDF content
    assert extractor._needs_ocr("") is True
    assert extractor._needs_ocr("a" * 200) is False

def test_structured_data_extraction(extractor):
    # Test the structure of the extracted data
    test_text = "Sample invoice text"
    result = extractor._extract_structured_data(test_text)
    
    assert isinstance(result, dict)
    assert "invoice_number" in result
    assert "date" in result
    assert "total_amount" in result
    assert "vendor_name" in result
    assert "line_items" in result 