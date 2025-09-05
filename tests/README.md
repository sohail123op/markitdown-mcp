# Test Structure

This directory will contain the comprehensive test suite for the MarkItDown MCP server.

## Proposed Directory Structure

```
tests/
├── unit/                           # Unit tests
│   ├── test_mcp_protocol.py        # MCP request/response handling
│   ├── test_server.py              # Server class functionality
│   ├── test_tools.py               # Individual tool testing
│   └── test_utils.py               # Utility functions
├── integration/                    # Integration tests
│   ├── test_mcp_server.py          # Full MCP server testing
│   ├── test_file_conversion.py     # End-to-end conversion testing
│   └── test_claude_integration.py  # Claude Desktop integration
├── performance/                    # Performance tests
│   ├── test_large_files.py         # Large file handling
│   ├── test_concurrent.py          # Concurrent request handling
│   └── test_memory_usage.py        # Memory efficiency testing
├── security/                       # Security tests
│   ├── test_path_traversal.py      # Path traversal protection
│   ├── test_malicious_files.py     # Malicious file handling
│   └── test_dos_protection.py      # DoS protection
├── compatibility/                  # Cross-platform tests
│   ├── test_platforms.py           # OS-specific testing
│   ├── test_dependencies.py        # Dependency variations
│   └── test_python_versions.py     # Python version compatibility
├── fixtures/                       # Test data
│   ├── documents/                  # Sample documents
│   │   ├── pdf/                    # PDF test files
│   │   ├── office/                 # Office document samples
│   │   ├── images/                 # Image files
│   │   ├── audio/                  # Audio samples
│   │   └── corrupted/              # Intentionally broken files
│   ├── expected_outputs/           # Expected conversion results
│   └── malicious/                  # Security test files (safe samples)
├── conftest.py                     # pytest configuration
├── test_data_generator.py          # Generate test files
└── helpers/                        # Test utilities
    ├── __init__.py
    ├── mcp_client.py              # Mock MCP client for testing
    ├── file_utils.py              # File manipulation helpers
    └── assertions.py              # Custom assertion helpers
```

## Test Categories

### 1. Unit Tests (`tests/unit/`)
- Test individual functions and methods in isolation
- Mock external dependencies
- Fast execution (< 1 second each)
- High coverage of edge cases

### 2. Integration Tests (`tests/integration/`)
- Test component interactions
- Real file system operations
- MCP protocol compliance
- Moderate execution time (1-10 seconds each)

### 3. Performance Tests (`tests/performance/`)
- Measure execution time and memory usage
- Test with large files and datasets
- Concurrent operation testing
- Long execution time acceptable

### 4. Security Tests (`tests/security/`)
- Input validation testing
- Path traversal attempts
- Malicious file handling
- DoS protection verification

### 5. Compatibility Tests (`tests/compatibility/`)
- Cross-platform testing
- Python version compatibility
- Dependency variation testing
- Environment-specific tests

## Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/unit/                  # Unit tests only
pytest tests/integration/          # Integration tests only
pytest tests/performance/          # Performance tests only

# Run tests with coverage
pytest --cov=markitdown_mcp tests/

# Run tests with verbose output
pytest -v tests/

# Run specific test files
pytest tests/unit/test_tools.py
pytest tests/integration/test_file_conversion.py

# Run tests matching a pattern
pytest -k "test_pdf" tests/        # All PDF-related tests
pytest -k "test_convert_file" tests/ # All convert_file tests
```

## Test Data Management

### Sample Files
- **Size categories**: Small (< 1KB), Medium (1KB-10MB), Large (> 10MB)
- **Format coverage**: All 29+ supported formats
- **Special cases**: Unicode filenames, spaces, symbols
- **Edge cases**: Empty files, minimal content, maximum size

### Expected Outputs
- Pre-generated expected results for deterministic tests
- Checksum validation for binary outputs
- Content structure validation for text outputs

### Security Test Files
- Safe samples of potentially malicious patterns
- Path traversal test cases
- Large file samples for DoS testing
- Zip bombs and recursive archives

## Continuous Integration

### GitHub Actions Workflow
```yaml
# Proposed CI pipeline
- Unit tests on multiple Python versions (3.10, 3.11, 3.12, 3.13)
- Integration tests on multiple OS (Ubuntu, Windows, macOS)
- Performance benchmarking with trend analysis
- Security scanning with static analysis
- Coverage reporting with codecov
- Documentation testing
```

### Test Automation
- Automated test discovery and execution
- Parallel test execution for performance
- Test result reporting and analysis
- Failure notification and debugging info

## Quality Gates

### Before Merge
- ✅ All unit tests pass
- ✅ Integration tests pass
- ✅ Code coverage > 90%
- ✅ No security vulnerabilities detected
- ✅ Performance benchmarks within limits

### Before Release
- ✅ Full test suite passes on all target platforms
- ✅ Performance tests complete successfully
- ✅ Security tests pass
- ✅ Manual testing validation complete
- ✅ Claude Desktop integration verified