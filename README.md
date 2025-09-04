# MDConvert

A powerful CLI tool that converts 29+ file formats to Markdown using Microsoft's MarkItDown library. 

**Perfect for:**
- 📄 Document processing workflows
- 🤖 Preparing content for LLMs
- 📚 Converting legacy documents to Markdown
- 🔄 Batch processing entire directories

Transform documents, images, audio, and more into clean, structured Markdown with OCR, speech recognition, and intelligent formatting.

## Features

- Convert multiple file formats to Markdown
- Batch processing of entire directories
- Preserves directory structure in output
- Environment variable support via .env file

## Supported File Formats

**Office Documents:**
- PDF files (.pdf)
- Word documents (.docx)
- PowerPoint presentations (.pptx)
- Excel spreadsheets (.xlsx, .xls)

**Web and Markup:**
- HTML files (.html, .htm)

**Data Formats:**
- CSV files (.csv)
- JSON files (.json)
- XML files (.xml)

**Archives:**
- ZIP files (.zip)

**E-books:**
- EPUB files (.epub)

**Images:**
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- WebP (.webp)

**Audio:**
- MP3 (.mp3)
- WAV (.wav)
- FLAC (.flac)
- M4A (.m4a)
- OGG (.ogg)
- WMA (.wma)

**Text Files:**
- Plain text (.txt)
- Markdown (.md)
- reStructuredText (.rst)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd mdconvert
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Convert a single file
python mdconvert.py --file document.pdf

# Convert all files in a directory
python mdconvert.py --input ./docs --output ./markdown
```

## Configuration

No special configuration required. The tool uses the MarkItDown library for document conversion.

## Usage

### Basic Usage

```bash
# Convert all supported files from input/ to output/
python mdconvert.py
```

### Custom Directories

Specify custom input and output directories:
```bash
python mdconvert.py --input /path/to/docs --output /path/to/markdown
```

### Single File Conversion

Convert a single file:
```bash
python mdconvert.py --file document.pdf
```

## Command Line Options

- `--input, -i`: Input directory (default: `input`)
- `--output, -o`: Output directory (default: `output`)
- `--file, -f`: Convert a single file instead of a directory

## Directory Structure

```
mdconvert/
├── mdconvert.py         # Main CLI script
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── input/              # Default input directory
└── output/             # Default output directory
```

## Requirements

- Python 3.8+
- See `requirements.txt` for Python package dependencies


## Notes

- The tool preserves the directory structure when converting files
- Output files are saved with the `.md` extension
- Images are processed with OCR and caption generation
- Audio files are processed with speech recognition
- ZIP files are extracted and their contents processed
- Some formats may require additional dependencies (automatically handled by MarkItDown)