import click
from pathlib import Path
from .extractor import InvoiceExtractor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.group()
def cli():
    """PDF Invoice Extraction System"""
    pass

@cli.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--gpu/--no-gpu', default=False, help='Use GPU for OCR processing')
def process(input, output, gpu):
    """Process a single PDF file."""
    try:
        extractor = InvoiceExtractor(use_gpu=gpu)
        result = extractor.process_pdf(input)
        
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                import json
                json.dump(result, f, indent=2)
            logger.info(f"Results saved to {output}")
        else:
            import json
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise click.Abort()

@cli.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument('output_dir', type=click.Path(file_okay=False, dir_okay=True))
@click.option('--gpu/--no-gpu', default=False, help='Use GPU for OCR processing')
def batch(input_dir, output_dir, gpu):
    """Process multiple PDF files in a directory."""
    try:
        extractor = InvoiceExtractor(use_gpu=gpu)
        extractor.process_batch(input_dir, output_dir)
        logger.info(f"Batch processing complete. Results saved to {output_dir}")
    except Exception as e:
        logger.error(f"Error processing batch: {str(e)}")
        raise click.Abort()

if __name__ == '__main__':
    cli() 