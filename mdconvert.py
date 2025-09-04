#!/usr/bin/env python3
"""
Document Transformer - Converts PDF and PPTX files to Markdown using Markitdown
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, List
import argparse
from markitdown import MarkItDown
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DocumentTransformer:
    def __init__(self):
        """
        Initialize the DocumentTransformer with Markitdown.
        """
        self.markitdown = MarkItDown()
    
    
    def convert_file(self, input_path: Path, output_path: Path) -> bool:
        """
        Convert a single file to Markdown.
        
        Args:
            input_path: Path to the input file
            output_path: Path for the output Markdown file
            
        Returns:
            True if conversion was successful, False otherwise
        """
        try:
            logger.info(f"Converting {input_path} to {output_path}")
            
            result = self.markitdown.convert(str(input_path))
            markdown_content = result.text_content
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logger.info(f"Successfully converted {input_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error converting {input_path}: {e}")
            return False
    
    def process_directory(self, input_dir: Path, output_dir: Path) -> tuple[int, int]:
        """
        Process all supported files in a directory.
        
        Args:
            input_dir: Path to input directory
            output_dir: Path to output directory
            
        Returns:
            Tuple of (successful conversions, failed conversions)
        """
        # All file formats supported by MarkItDown
        supported_extensions = {
            # Office documents
            '.pdf', '.docx', '.pptx', '.xlsx', '.xls',
            # Web and markup
            '.html', '.htm',
            # Data formats
            '.csv', '.json', '.xml',
            # Archives
            '.zip',
            # E-books
            '.epub',
            # Images (common formats)
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp',
            # Audio (common formats)
            '.mp3', '.wav', '.flac', '.m4a', '.ogg', '.wma',
            # Text files
            '.txt', '.md', '.rst'
        }
        success_count = 0
        failed_count = 0
        
        for file_path in input_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                relative_path = file_path.relative_to(input_dir)
                output_path = output_dir / relative_path.with_suffix('.md')
                
                if self.convert_file(file_path, output_path):
                    success_count += 1
                else:
                    failed_count += 1
        
        return success_count, failed_count


def main():
    parser = argparse.ArgumentParser(description='Convert various file formats to Markdown using MarkItDown')
    parser.add_argument('--input', '-i', type=str, default='input',
                        help='Input directory containing supported files (default: input)')
    parser.add_argument('--output', '-o', type=str, default='output',
                        help='Output directory for Markdown files (default: output)')
    parser.add_argument('--file', '-f', type=str,
                        help='Convert a single file instead of processing a directory')
    
    args = parser.parse_args()
    
    # Load .env file if it exists
    load_dotenv()
    
    transformer = DocumentTransformer()
    
    if args.file:
        input_path = Path(args.file)
        if not input_path.exists():
            logger.error(f"File not found: {input_path}")
            sys.exit(1)
        
        output_path = Path(args.output) / input_path.with_suffix('.md').name
        success = transformer.convert_file(input_path, output_path)
        
        if success:
            logger.info(f"Conversion completed. Output saved to: {output_path}")
        else:
            logger.error("Conversion failed")
            sys.exit(1)
    else:
        input_dir = Path(args.input)
        output_dir = Path(args.output)
        
        if not input_dir.exists():
            logger.error(f"Input directory not found: {input_dir}")
            sys.exit(1)
        
        logger.info(f"Processing files from {input_dir} to {output_dir}")
        success_count, failed_count = transformer.process_directory(
            input_dir, output_dir
        )
        
        logger.info(f"Conversion completed: {success_count} successful, {failed_count} failed")
        
        if failed_count > 0:
            sys.exit(1)


if __name__ == '__main__':
    main()