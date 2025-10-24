# Test Suite Documentation

This directory contains the comprehensive test suite for the mcp-md-pdf converter.

## Overview

The test suite validates all aspects of the markdown to Word/PDF conversion process, including:
- Core conversion functionality
- Markdown element handling
- Template support
- MCP server tools
- Error handling and edge cases

## Test Structure

```
tests/
├── __init__.py           # Makes tests directory a Python package
├── conftest.py           # Pytest fixtures and shared test utilities
├── test_converter.py     # Tests for MarkdownConverter class
├── test_server.py        # Tests for MCP server tools
└── README.md             # This file
```

## Running Tests

### Run All Tests

```bash
# From project root
pytest

# With verbose output
pytest -v

# With coverage report
pytest --cov=src/md_pdf_mcp --cov-report=html
```

### Run Specific Test Files

```bash
# Test converter only
pytest tests/test_converter.py

# Test MCP server only
pytest tests/test_server.py
```

### Run Specific Test Classes or Functions

```bash
# Run a specific test class
pytest tests/test_converter.py::TestMarkdownToWord

# Run a specific test function
pytest tests/test_converter.py::TestMarkdownToWord::test_basic_conversion

# Run tests matching a pattern
pytest -k "test_bold"
```

### Run Tests by Markers

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## Test Categories

### 1. Converter Tests (`test_converter.py`)

#### TestMarkdownToWord
Tests basic markdown to Word conversion functionality.

**Tests:**
- `test_basic_conversion` - Basic markdown file conversion
- `test_simple_conversion` - Simple markdown with minimal features
- `test_emoji_support` - Unicode and emoji character support
- `test_nonexistent_markdown_file` - Error handling for missing files
- `test_output_directory_created` - Output directory creation

#### TestDocumentContent
Validates that converted documents contain expected content.

**Tests:**
- `test_headings_present` - All heading levels are converted
- `test_text_content_present` - Text content preservation
- `test_tables_converted` - Markdown tables → Word tables
- `test_bullet_lists_converted` - Bullet list formatting
- `test_numbered_lists_converted` - Numbered list formatting

#### TestTextFormatting
Tests inline text formatting (bold, italic, code).

**Tests:**
- `test_bold_formatting` - **Bold** text conversion
- `test_italic_formatting` - *Italic* text conversion

#### TestTemplateSupport
Tests .dotx template loading and application.

**Tests:**
- `test_conversion_without_template` - Default styling
- `test_nonexistent_template` - Missing template handling

#### TestEdgeCases
Tests edge cases and special scenarios.

**Tests:**
- `test_empty_markdown` - Empty file handling
- `test_markdown_with_only_whitespace` - Whitespace-only files
- `test_nested_lists` - Nested bullet and numbered lists
- `test_code_block_preservation` - Code blocks don't convert to lists

#### TestPDFConversion
Tests PDF conversion functionality (requires Microsoft Word).

**Tests:**
- `test_word_to_pdf_requires_word` - PDF conversion with/without Word

### 2. Server Tests (`test_server.py`)

#### TestConvertMarkdownTool
Tests the `convert_markdown` MCP tool.

**Tests:**
- `test_convert_to_docx` - DOCX output format
- `test_convert_to_both` - Both DOCX and PDF output
- `test_nonexistent_markdown` - Error handling for missing input
- `test_nonexistent_template` - Error handling for missing template
- `test_output_directory_creation` - Output directory handling
- `test_pdf_only_output` - PDF-only output (temp DOCX cleanup)

#### TestConvertMarkdownBatchTool
Tests the `convert_markdown_batch` MCP tool.

**Tests:**
- `test_batch_conversion_success` - Batch processing multiple files
- `test_batch_with_missing_files` - Partial batch failures
- `test_batch_with_nonexistent_template` - Template validation
- `test_empty_batch` - Empty file list handling

#### TestListSupportedFormatsTool
Tests the `list_supported_formats` MCP tool.

**Tests:**
- `test_list_formats_returns_info` - Format information returned
- `test_list_formats_mentions_features` - Feature documentation
- `test_list_formats_mentions_platform_notes` - Platform notes

## Test Fixtures

Fixtures are defined in `conftest.py` and provide reusable test data and utilities.

### Available Fixtures

#### `temp_dir`
Creates a temporary directory for test outputs. Automatically cleaned up after test.

**Usage:**
```python
def test_example(temp_dir):
    output_file = os.path.join(temp_dir, "output.docx")
    # Use temp_dir for test files
```

#### `sample_markdown`
Creates a comprehensive markdown file testing all features.

**Contains:**
- All heading levels (H1-H6)
- Text formatting (bold, italic, code)
- Bullet and numbered lists
- Code blocks
- Blockquotes
- Tables
- Horizontal rules

**Usage:**
```python
def test_example(sample_markdown):
    # sample_markdown is path to temp markdown file
    converter.markdown_to_word(sample_markdown, output_path)
```

#### `simple_markdown`
Creates a simple markdown file for basic tests.

**Contains:**
- Simple heading
- Bullet list
- Numbered list

#### `markdown_with_emoji`
Creates markdown with emoji and special characters.

**Contains:**
- Emoji (✅ ❌ 🔥)
- Unicode characters (Chinese, Arabic)

#### `output_docx_path`
Generates output path for DOCX files in temp directory.

#### `output_pdf_path`
Generates output path for PDF files in temp directory.

## What Each Test Tests

### Conversion Accuracy Tests

These tests verify that markdown elements convert correctly:

1. **Heading Conversion** (`test_headings_present`)
   - ✅ All heading levels (H1-H6) are created
   - ✅ Heading text is preserved
   - ✅ Fallback to formatted text for H4-H6 if template lacks styles

2. **List Conversion** (`test_bullet_lists_converted`, `test_numbered_lists_converted`)
   - ✅ Bullet lists use bullet formatting (not numbers)
   - ✅ Numbered lists use sequential numbering
   - ✅ Numbering restarts after headings
   - ✅ Nested lists maintain hierarchy

3. **Table Conversion** (`test_tables_converted`)
   - ✅ Markdown tables → Word tables
   - ✅ Header row is formatted (bold, shading)
   - ✅ Inline formatting in cells preserved (**bold**, *italic*, `code`)

4. **Text Formatting** (`test_bold_formatting`, `test_italic_formatting`)
   - ✅ **Bold** converts to bold runs
   - ✅ *Italic* converts to italic runs
   - ✅ `Code` converts to monospace

### Robustness Tests

These tests verify error handling and edge cases:

1. **Missing Files** (`test_nonexistent_markdown_file`, `test_nonexistent_template`)
   - ✅ Graceful error messages
   - ✅ No crashes on missing input
   - ✅ Template is optional

2. **Edge Cases** (`test_empty_markdown`, `test_markdown_with_only_whitespace`)
   - ✅ Empty files don't crash
   - ✅ Whitespace-only files handled
   - ✅ Output files still created

3. **Code Block Preservation** (`test_code_block_preservation`)
   - ✅ Numbers in code blocks stay as text (not converted to lists)
   - ✅ Bullets in code blocks stay as text

### Integration Tests

These tests verify end-to-end workflows:

1. **MCP Tool Tests** (all tests in `test_server.py`)
   - ✅ Tools return proper success/error messages
   - ✅ Files are created in correct locations
   - ✅ Batch processing handles partial failures
   - ✅ Output format parameter works correctly

2. **Template Integration** (`test_conversion_without_template`)
   - ✅ Conversion works with or without template
   - ✅ Template styles are applied when present
   - ✅ Bullet numbering created even with template

## Test Data

Test markdown files are created dynamically using fixtures. Here's what they contain:

### Sample Markdown Structure

```markdown
# Test Document

## Features Tested

### Headings
H1, H2, H3 tested.

#### H4 Heading
H4 support.

### Text Formatting
**bold**, *italic*, `code`

### Lists
- Bullet 1
- Bullet 2

1. Number 1
2. Number 2

### Code Blocks
```python
def hello():
    print("Hi")
```

### Tables
| Col 1 | Col 2 |
|-------|-------|
| Data  | More  |
```

## Expected Test Results

### When All Tests Pass

```
================================ test session starts ================================
tests/test_converter.py ...............................                      [68%]
tests/test_server.py .......................                                [100%]

========================= 54 passed in 2.34s =========================
```

### Understanding Test Failures

#### Example: Table Test Failure

```
FAILED tests/test_converter.py::TestDocumentContent::test_tables_converted

AssertionError: No tables found in document
```

**What this means**: The table parsing or Word table creation is broken.

**How to debug**:
1. Run the specific test: `pytest tests/test_converter.py::TestDocumentContent::test_tables_converted -v`
2. Check the converter's `_parse_markdown_table()` and `_add_word_table()` methods
3. Verify table detection pattern in `_parse_markdown_line()`

#### Example: Bold Formatting Failure

```
FAILED tests/test_converter.py::TestTextFormatting::test_bold_formatting

AssertionError: Bold formatting not found in document
```

**What this means**: `**bold**` text not converting to bold runs.

**How to debug**:
1. Check `_add_formatted_text()` method
2. Verify bold pattern regex: `r'\*\*(.*?)\*\*'`
3. Test manually with simple markdown

## Coverage Goals

Current coverage targets:
- **Converter**: 90%+ coverage
- **Server**: 85%+ coverage
- **Overall**: 85%+ coverage

View coverage report:
```bash
pytest --cov=src/md_pdf_mcp --cov-report=html
# Open htmlcov/index.html in browser
```

## Adding New Tests

### When to Add Tests

Add tests when:
1. Adding new markdown features
2. Fixing a bug (add regression test)
3. Adding new MCP tools
4. Changing conversion behavior

### How to Add Tests

1. **Choose the right test file**:
   - Converter functionality → `test_converter.py`
   - MCP tools → `test_server.py`

2. **Use existing fixtures** from `conftest.py` or create new ones

3. **Follow naming conventions**:
   - Test classes: `TestFeatureName`
   - Test functions: `test_what_it_tests`

4. **Add docstrings** explaining what the test validates

### Example: Adding a New Test

```python
# In test_converter.py

class TestNewFeature:
    """Test new feature functionality"""

    def test_feature_works(self, sample_markdown, output_docx_path):
        """Test that new feature converts correctly"""
        converter = MarkdownConverter()

        result = converter.markdown_to_word(sample_markdown, output_docx_path)

        assert result is True
        # Add specific assertions for new feature
```

## Common Issues

### 1. PDF Tests Fail

**Issue**: PDF conversion tests fail with "pywin32 required" or "Word not found"

**Solution**: This is expected if Microsoft Word is not installed. The test handles this gracefully.

### 2. Temp Files Not Cleaned Up

**Issue**: Test temp files accumulate

**Solution**: The `temp_dir` fixture automatically cleans up. If tests are interrupted (Ctrl+C), manually delete temp folders starting with `md_pdf_test_`.

### 3. Unicode Errors on Windows Console

**Issue**: Test output shows unicode encoding errors

**Solution**: This is a console display issue only. Tests still pass. Files are created correctly with UTF-8 encoding.

## Continuous Integration

For CI/CD pipelines (GitHub Actions, GitLab CI, etc.):

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -e ".[dev]"
    pytest --cov=src/md_pdf_mcp --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

## Contributing Tests

When contributing:
1. ✅ Write tests for new features
2. ✅ Ensure all tests pass locally
3. ✅ Maintain or improve coverage
4. ✅ Add docstrings to new tests
5. ✅ Update this README if adding new test categories

## Questions?

If you have questions about the tests:
1. Check this README
2. Look at existing test examples in `test_converter.py` and `test_server.py`
3. Review fixtures in `conftest.py`
4. Open an issue on GitHub
