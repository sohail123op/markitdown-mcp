# Known Issues

## Unicode Errors with Markdown Files

Some `.md` files may fail to convert with a `UnicodeDecodeError` when they contain non-ASCII characters. This is a known limitation in the MarkItDown library's `PlainTextConverter`, which uses ASCII encoding by default.

**Workaround**: Convert these files using a different method or wait for an upstream fix in the MarkItDown library.

**Affected error**:
```
PlainTextConverter threw UnicodeDecodeError with message: 'ascii' codec can't decode byte...
```

## Office File Dependencies

Excel (.xlsx, .xls) and PowerPoint (.pptx) files require additional dependencies. If you see errors like:

```
XlsxConverter threw MissingDependencyException...
PptxConverter threw BadZipFile...
```

**Solution**: Install the required dependencies using pipx:

```bash
pipx inject markitdown-mcp openpyxl xlrd pandas tabulate
```

## Corrupted Office Files

Some Office files may fail with `BadZipFile` errors if they are corrupted or use an incompatible format. This typically happens with files that:
- Are password protected
- Use very old Office formats
- Are corrupted or partially downloaded
- Were created with non-Microsoft Office software

**Solution**: Try opening and re-saving the file in Microsoft Office or a compatible application.

## Large File Timeouts

Very large files (especially PDFs with many pages) may cause timeouts in Claude Desktop. The default timeout is 2 minutes per file.

**Solution**: For batch conversions of large files, consider:
- Converting smaller batches at a time
- Using the tool directly from command line for very large files
- Splitting large PDFs into smaller chunks before conversion