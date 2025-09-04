# 📄 MarkItDown MCP Server

[![MCP](https://img.shields.io/badge/Model_Context_Protocol-MCP-blue)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A powerful **Model Context Protocol (MCP) server** that converts 29+ file formats to clean, structured Markdown using Microsoft's MarkItDown library.

🔥 **Perfect for Claude Desktop, MCP clients, and AI workflows!** 

## ✨ Features

- 🔌 **MCP Protocol**: Seamless integration with Claude Desktop and MCP clients
- 📁 **29+ File Formats**: PDFs, Office docs, images, audio, archives, and more
- 🔍 **OCR Support**: Extract text from images (JPG, PNG, GIF, BMP, TIFF, WebP)
- 🎵 **Speech Recognition**: Convert audio to text (MP3, WAV, FLAC, M4A, OGG, WMA)
- 📊 **Office Documents**: Word, PowerPoint, Excel files
- 🌐 **Web Content**: HTML, XML, JSON, CSV
- 📚 **E-books & Archives**: EPUB, ZIP files
- ⚡ **Fast & Reliable**: Built on Microsoft's MarkItDown library

## 🚀 Quick Start for Claude Desktop

1. **Install the server:**
   ```bash
   pip install -e git+https://github.com/trsdn/markitdown-mcp.git
   ```

2. **Add to your Claude Desktop config:**
   ```json
   {
     "mcpServers": {
       "markitdown": {
         "command": "markitdown-mcp",
         "args": []
       }
     }
   }
   ```

3. **Restart Claude Desktop** and start converting files!

## Features

- Convert multiple file formats to Markdown
- Batch processing of entire directories
- Preserves directory structure in output
- Environment variable support via .env file

## 📋 Available MCP Tools

### 🔧 `convert_file`
Convert a single file to Markdown.
```json
{
  "name": "convert_file",
  "arguments": {
    "file_path": "/path/to/document.pdf"
  }
}
```

### 📋 `list_supported_formats`
Get a complete list of supported file formats.
```json
{
  "name": "list_supported_formats",
  "arguments": {}
}
```

### 📁 `convert_directory`
Convert all supported files in a directory.
```json
{
  "name": "convert_directory", 
  "arguments": {
    "input_directory": "/path/to/files",
    "output_directory": "/path/to/markdown" 
  }
}
```

## 📄 Supported File Formats (29+)

| Category | Extensions | Features |
|----------|------------|----------|
| **📊 Office** | `.pdf`, `.docx`, `.pptx`, `.xlsx`, `.xls` | Full document structure |
| **🖼️ Images** | `.jpg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp` | OCR text extraction |
| **🎵 Audio** | `.mp3`, `.wav`, `.flac`, `.m4a`, `.ogg`, `.wma` | Speech-to-text |
| **🌐 Web** | `.html`, `.htm`, `.xml`, `.json`, `.csv` | Clean formatting |
| **📚 Books** | `.epub` | Chapter extraction |
| **📦 Archives** | `.zip` | Auto-extract and process |
| **📝 Text** | `.txt`, `.md`, `.rst` | Direct conversion |

## Installation

### Option 1: Pip Install (Recommended)

```bash
# Install from local directory
pip install -e /Users/torstenmahr/GitHub/markitdown-mcp

# Or navigate to the directory first
cd /Users/torstenmahr/GitHub/markitdown-mcp
pip install -e .
```

### Option 2: Direct Usage

```bash
cd /Users/torstenmahr/GitHub/markitdown-mcp
source venv/bin/activate
pip install -r requirements.txt
```

## Quick Start

### MCP Server Mode (Recommended)

After pip installation:
```bash
# Start the MCP server (for use with MCP clients)
markitdown-mcp
```

Or using the development script:
```bash
python run_server.py
```

## 🛠️ Installation Options

### For Claude Desktop Users (Recommended)
```bash
pip install -e git+https://github.com/trsdn/markitdown-mcp.git
```

### For Development
```bash
git clone https://github.com/trsdn/markitdown-mcp.git
cd markitdown-mcp
pip install -e .
```

## 🔧 Claude Desktop Configuration

Add this to your Claude Desktop `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "markitdown-mcp",
      "args": []
    }
  }
}
```

**Config file locations:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

## 💡 Usage Examples

### Convert a PDF
```
Convert the file ~/Documents/report.pdf to markdown
```

### Batch Process Directory
```
Convert all files in ~/Downloads/documents/ to markdown
```

### Check Supported Formats
```
What file formats can you convert to markdown?
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

## MCP Server Features

The MCP server provides three tools:

### 1. convert_file
Convert a single file to Markdown.
- **Input**: File path or base64 encoded content with filename
- **Output**: Converted Markdown content

### 2. list_supported_formats
List all supported file formats.
- **Output**: Categorized list of supported file extensions

### 3. convert_directory
Convert all supported files in a directory.
- **Input**: Input directory path, optional output directory
- **Output**: Summary of conversion results

## Directory Structure

```
markitdown-mcp/
├── mcp_server.py        # MCP protocol server
├── mdconvert.py         # CLI script
├── run_server.py        # Server runner script
├── mcp_config.json      # MCP configuration
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── input/              # Default input directory
├── output/             # Default output directory
└── venv/               # Virtual environment
```

## 🔍 How It Works

This MCP server leverages Microsoft's MarkItDown library to provide intelligent document conversion:

- **📄 PDFs**: Extracts text, tables, and structure
- **🖼️ Images**: Uses OCR to extract text content  
- **🎵 Audio**: Converts speech to text transcription
- **📊 Office**: Preserves formatting from Word, Excel, PowerPoint
- **🌐 HTML**: Converts to clean, readable Markdown
- **📦 Archives**: Automatically extracts and processes contents

## 🏷️ Tags

`mcp` `model-context-protocol` `claude-desktop` `markdown` `document-conversion` `pdf` `ocr` `speech-to-text` `markitdown` `ai-tools`

## 📋 Requirements

- **Python**: 3.8+
- **MCP Client**: Claude Desktop or compatible MCP client
- **Dependencies**: Automatically installed via pip

## 🤝 Contributing

Contributions welcome! Please feel free to submit issues and pull requests.

## 📄 License

MIT License - see LICENSE file for details.

## 🔗 Related

- [Model Context Protocol](https://modelcontextprotocol.io)
- [Claude Desktop](https://claude.ai/desktop)  
- [Microsoft MarkItDown](https://github.com/microsoft/markitdown)