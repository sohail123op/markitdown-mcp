#!/usr/bin/env python3
"""
MarkItDown MCP Server - Model Context Protocol server for document conversion
Converts various file formats to Markdown using Microsoft's MarkItDown library.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging
from markitdown import MarkItDown
from dataclasses import dataclass
import base64
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("markitdown-mcp")

@dataclass
class MCPRequest:
    id: str
    method: str
    params: Dict[str, Any]

@dataclass
class MCPResponse:
    id: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

class MarkItDownMCPServer:
    def __init__(self):
        self.markitdown = MarkItDown()
        self.supported_extensions = {
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

    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle incoming MCP requests"""
        try:
            if request.method == "initialize":
                return MCPResponse(
                    id=request.id,
                    result={
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "markitdown-server",
                            "version": "1.0.0"
                        }
                    }
                )
            
            elif request.method == "tools/list":
                return MCPResponse(
                    id=request.id,
                    result={
                        "tools": [
                            {
                                "name": "convert_file",
                                "description": "Convert a file to Markdown using MarkItDown",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "file_path": {
                                            "type": "string",
                                            "description": "Path to the file to convert"
                                        },
                                        "file_content": {
                                            "type": "string",
                                            "description": "Base64 encoded file content (alternative to file_path)"
                                        },
                                        "filename": {
                                            "type": "string",
                                            "description": "Original filename when using file_content"
                                        }
                                    },
                                    "anyOf": [
                                        {"required": ["file_path"]},
                                        {"required": ["file_content", "filename"]}
                                    ]
                                }
                            },
                            {
                                "name": "list_supported_formats",
                                "description": "List all supported file formats for conversion",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {}
                                }
                            },
                            {
                                "name": "convert_directory",
                                "description": "Convert all supported files in a directory to Markdown",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "input_directory": {
                                            "type": "string",
                                            "description": "Path to the input directory"
                                        },
                                        "output_directory": {
                                            "type": "string",
                                            "description": "Path to the output directory (optional)"
                                        }
                                    },
                                    "required": ["input_directory"]
                                }
                            }
                        ]
                    }
                )
            
            elif request.method == "tools/call":
                tool_name = request.params.get("name")
                arguments = request.params.get("arguments", {})
                
                if tool_name == "convert_file":
                    return await self.convert_file_tool(request.id, arguments)
                elif tool_name == "list_supported_formats":
                    return await self.list_supported_formats_tool(request.id)
                elif tool_name == "convert_directory":
                    return await self.convert_directory_tool(request.id, arguments)
                else:
                    return MCPResponse(
                        id=request.id,
                        error={"code": -32601, "message": f"Unknown tool: {tool_name}"}
                    )
            
            else:
                return MCPResponse(
                    id=request.id,
                    error={"code": -32601, "message": f"Unknown method: {request.method}"}
                )
                
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return MCPResponse(
                id=request.id,
                error={"code": -32603, "message": f"Internal error: {str(e)}"}
            )

    async def convert_file_tool(self, request_id: str, arguments: Dict[str, Any]) -> MCPResponse:
        """Convert a single file to Markdown"""
        try:
            file_path = arguments.get("file_path")
            file_content = arguments.get("file_content")
            filename = arguments.get("filename")
            
            if file_path:
                # Convert from file path
                path = Path(file_path)
                if not path.exists():
                    return MCPResponse(
                        request_id,
                        error={"code": -32602, "message": f"File not found: {file_path}"}
                    )
                
                result = self.markitdown.convert(str(path))
                markdown_content = result.text_content
                
                return MCPResponse(
                    request_id,
                    result={
                        "content": [
                            {
                                "type": "text",
                                "text": f"Successfully converted {path.name} to Markdown:\n\n{markdown_content}"
                            }
                        ]
                    }
                )
                
            elif file_content and filename:
                # Convert from base64 encoded content
                try:
                    # Decode base64 content
                    decoded_content = base64.b64decode(file_content)
                    
                    # Create temporary file
                    with tempfile.NamedTemporaryFile(suffix=Path(filename).suffix, delete=False) as temp_file:
                        temp_file.write(decoded_content)
                        temp_path = temp_file.name
                    
                    try:
                        result = self.markitdown.convert(temp_path)
                        markdown_content = result.text_content
                        
                        return MCPResponse(
                            request_id,
                            result={
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"Successfully converted {filename} to Markdown:\n\n{markdown_content}"
                                    }
                                ]
                            }
                        )
                    finally:
                        # Clean up temporary file
                        Path(temp_path).unlink(missing_ok=True)
                        
                except Exception as e:
                    return MCPResponse(
                        request_id,
                        error={"code": -32602, "message": f"Error processing file content: {str(e)}"}
                    )
            else:
                return MCPResponse(
                    request_id,
                    error={"code": -32602, "message": "Either file_path or (file_content + filename) required"}
                )
                
        except Exception as e:
            logger.error(f"Error in convert_file_tool: {e}")
            return MCPResponse(
                request_id,
                error={"code": -32603, "message": f"Conversion failed: {str(e)}"}
            )

    async def list_supported_formats_tool(self, request_id: str) -> MCPResponse:
        """List all supported file formats"""
        format_categories = {
            "Office Documents": [".pdf", ".docx", ".pptx", ".xlsx", ".xls"],
            "Web and Markup": [".html", ".htm"],
            "Data Formats": [".csv", ".json", ".xml"],
            "Archives": [".zip"],
            "E-books": [".epub"],
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp"],
            "Audio": [".mp3", ".wav", ".flac", ".m4a", ".ogg", ".wma"],
            "Text Files": [".txt", ".md", ".rst"]
        }
        
        format_list = []
        for category, extensions in format_categories.items():
            format_list.append(f"**{category}:**")
            for ext in extensions:
                format_list.append(f"  - {ext}")
            format_list.append("")
        
        return MCPResponse(
            request_id,
            result={
                "content": [
                    {
                        "type": "text",
                        "text": "Supported file formats for MarkItDown conversion:\n\n" + "\n".join(format_list)
                    }
                ]
            }
        )

    async def convert_directory_tool(self, request_id: str, arguments: Dict[str, Any]) -> MCPResponse:
        """Convert all supported files in a directory"""
        try:
            input_dir = Path(arguments["input_directory"])
            output_dir = Path(arguments.get("output_directory", input_dir / "converted_markdown"))
            
            if not input_dir.exists():
                return MCPResponse(
                    request_id,
                    error={"code": -32602, "message": f"Input directory not found: {input_dir}"}
                )
            
            success_count = 0
            failed_count = 0
            failed_files = []
            
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for file_path in input_dir.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                    try:
                        relative_path = file_path.relative_to(input_dir)
                        output_path = output_dir / relative_path.with_suffix('.md')
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        result = self.markitdown.convert(str(file_path))
                        markdown_content = result.text_content
                        
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(markdown_content)
                        
                        success_count += 1
                        
                    except Exception as e:
                        failed_count += 1
                        failed_files.append(f"{file_path.name}: {str(e)}")
            
            result_text = f"Directory conversion completed:\n"
            result_text += f"- Successfully converted: {success_count} files\n"
            result_text += f"- Failed conversions: {failed_count} files\n"
            result_text += f"- Output directory: {output_dir}\n"
            
            if failed_files:
                result_text += f"\nFailed files:\n"
                for failed in failed_files[:10]:  # Limit to first 10 failures
                    result_text += f"  - {failed}\n"
                if len(failed_files) > 10:
                    result_text += f"  ... and {len(failed_files) - 10} more\n"
            
            return MCPResponse(
                request_id,
                result={
                    "content": [
                        {
                            "type": "text",
                            "text": result_text
                        }
                    ]
                }
            )
            
        except Exception as e:
            logger.error(f"Error in convert_directory_tool: {e}")
            return MCPResponse(
                request_id,
                error={"code": -32603, "message": f"Directory conversion failed: {str(e)}"}
            )

    async def run(self):
        """Run the MCP server"""
        logger.info("MarkItDown MCP Server starting...")
        
        try:
            while True:
                # Read JSON-RPC message from stdin
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                
                if not line:
                    break
                
                try:
                    message = json.loads(line.strip())
                    request = MCPRequest(
                        id=message.get("id", "unknown"),
                        method=message["method"],
                        params=message.get("params", {})
                    )
                    
                    response = await self.handle_request(request)
                    
                    # Send response
                    response_dict = {"jsonrpc": "2.0", "id": response.id}
                    if response.result is not None:
                        response_dict["result"] = response.result
                    if response.error is not None:
                        response_dict["error"] = response.error
                    
                    print(json.dumps(response_dict), flush=True)
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON received: {e}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}")

def main():
    """Main entry point for console script"""
    async def run_server():
        server = MarkItDownMCPServer()
        await server.run()
    
    asyncio.run(run_server())

if __name__ == "__main__":
    main()