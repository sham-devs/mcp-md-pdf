# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**MD-PDF-MCP** is a Model Context Protocol (MCP) server that converts Markdown files to Word (.docx) and PDF documents with professional styling and optional .dotx template support.

**Key Architecture:**

- **FastMCP Server** (`src/md_pdf_mcp/server.py`): Exposes 3 MCP tools for AI assistants
- **Markdown Converter** (`src/md_pdf_mcp/converter.py`): Core conversion engine using python-docx
- **XML Styling System**: Uses OpenXML (via `OxmlElement`) for professional document styling

## Development Commands

### Installation

```bash
# Development install (editable mode)
pip install -e .

# With dev dependencies
pip install -e ".[dev]"
```

### Testing

```bash
# Run all tests
pytest

# Run tests excluding slow ones (e.g., PDF conversion)
pytest -m "not slow"

# Run specific test file
pytest tests/test_converter.py

# Run specific test
pytest tests/test_converter.py::TestDocumentContent::test_headings_present

# Run with coverage
pytest --cov=src/md_pdf_mcp --cov-report=html

# Run verbose with short traceback
pytest -v --tb=short
```

**Test Markers:**

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Long-running tests (PDF conversion)
- `@pytest.mark.requires_word` - Requires Microsoft Word

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/
```

### Running the MCP Server

```bash
# Run server directly
python -m md_pdf_mcp.server

# Test with MCP Inspector
npx @modelcontextprotocol/inspector python -m md_pdf_mcp.server
```

## Architecture Details

### Two-Layer Conversion System

1. **MCP Layer** (`server.py`):
   - Exposes tools: `convert_markdown`, `convert_markdown_batch`, `list_supported_formats`
   - Handles validation, file I/O, error messaging
   - Shared internal function `_convert_markdown_impl()` for DRY

2. **Converter Layer** (`converter.py`):
   - `markdown_to_word()`: Markdown → .docx using python-docx
   - `word_to_pdf()`: .docx → .pdf (cross-platform: MS Word on Windows, LibreOffice on Linux/macOS)
   - `_word_to_pdf_windows()`: MS Word COM automation implementation
   - `_word_to_pdf_libreoffice()`: LibreOffice headless mode implementation
   - Template support via `_load_template()`

### Markdown Processing Pipeline

The converter uses a **two-pass parsing system**:

**Pass 1: Line-by-line parsing** (`_parse_markdown_line()`)

- Identifies element type: heading, list, code block, table, quote, HR
- Returns `(style_type, content, metadata)`
- Handles nesting contexts (code blocks, tables)

**Pass 2: Document building** (`markdown_to_word()`)

- Creates Word elements based on parsed styles
- Applies professional styling (borders, backgrounds, fonts)
- Manages list numbering restart logic
- Handles inline formatting (bold, italic, code)

**Critical State Tracking:**

- `in_code_block`: Tracks code fence boundaries
- `in_table`: Accumulates table rows before rendering
- `current_list_level`: Manages nested list indentation
- `prev_style_type`: Detects list interruptions for numbering restart

### Professional Styling System

Uses OpenXML manipulation for visual polish:

**Helper Methods:**

- `_add_paragraph_shading(paragraph, color)`: Background colors
- `_add_paragraph_border(paragraph, positions, size, color)`: Borders
- `_add_run_shading(run, color)`: Inline code backgrounds

**Applied Styling:**

- **Code blocks**: `#F5F5F5` background, `#CCCCCC` border
- **Blockquotes**: Italic text, `#F9F9F9` background, `#4A90E2` left border (3pt)
- **Inline code**: `#F5F5F5` background
- **Table headers**: Bold, `#D9E2F3` background

### List Numbering Restart Logic

**Critical Feature** (`_restart_list_numbering()`):

- Detects when numbered lists are interrupted by non-list elements
- Creates new `AbstractNum` ID in Word's numbering system
- Prevents numbering continuation across document sections
- Implementation: Lines 314-370 in `converter.py`

### Template System

Templates (`.dotx` files) provide:

- Custom heading styles (H1-H6)
- Font families and sizes
- Page margins, headers/footers
- Color schemes

**Fallback behavior:**

- If template lacks heading styles → Uses formatted paragraphs with bold
- Always creates bullet numbering (`_create_bullet_numbering()`) even with templates

## Important Constraints

### File Handling

- **DO NOT create markdown files in project root** - Use `docs/` for documentation
- Test output files (`.docx`, `.pdf`) are gitignored

### Platform Requirements

- **DOCX conversion**: Cross-platform (python-docx works everywhere)
- **PDF conversion**: Cross-platform with platform-specific backends
  - **Windows**: Requires Microsoft Word (uses COM automation via pywin32)
  - **macOS**: Requires LibreOffice (`brew install --cask libreoffice`)
  - **Linux**: Requires LibreOffice (`sudo apt-get install libreoffice`)

### Testing Considerations

- Use `temp_dir` fixture for test outputs (auto-cleanup)
- Fixtures: `sample_markdown`, `simple_markdown`, `markdown_with_emoji`
- PDF tests should be marked `@pytest.mark.slow` or `@pytest.mark.requires_word`

## Key Implementation Notes

### Inline Formatting Parser

- Uses regex to split text on formatting markers: `**bold**`, `*italic*`, `` `code` ``
- Handles nested formatting: `**bold with *italic***`
- Pattern: `re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`)', text)`

### H4-H6 Heading Support

- Templates may not define H4-H6 styles
- Fallback: Creates formatted paragraphs with:
  - Bold text
  - Decreasing font sizes (14pt → 12pt → 11pt)
  - Proper spacing

### Table Rendering

- Accumulates rows in `in_table` list
- Renders complete table when table block ends
- Inline formatting preserved in cells
- Header row: Bold + colored background

## Testing Strategy

**100+ tests covering:**

- Core conversion (headings, lists, code, tables)
- Edge cases (empty tables, deeply nested lists, Unicode)
- Security (path traversal, XXS in markdown)
- Error handling (missing files, invalid templates)
- Platform-specific (PDF on Windows)

**Key test files:**

- `test_converter.py`: Core conversion functionality
- `test_advanced_markdown.py`: Extended features (H4-H6, nested lists, task lists)
- `test_tables_advanced.py`: Table edge cases (13 tests)
- `test_boundary_conditions.py`: Unicode, large files, deep nesting
- `test_security.py`: Path traversal, XSS prevention

## Documentation Structure

- `README.md`: User-focused quick start (410 lines)
- `docs/MARKDOWN_COVERAGE.md`: Technical feature analysis (687 lines)
  - CommonMark 0.31.2 compliance (70%)
  - GitHub Flavored Markdown support
  - Visual styling implementation details
- <!-- # Sequential Thinking Prompt Rules -->
<!-- # Purpose: Keep the agent organized, self-aware, and able to recover intelligently when facing complex or repetitive challenges. -->

## rules must consider always

- At the beginning of every user request, organize your workflow as follows:
      1. After planning and before any major action, call `vibe_check`.
      2. Output the full user request and your current plan.
      3. Optionally, record any resolved issues with `vibe_learn`.

- If a problem persists after two failed attempts, automatically invoke **Sequential Thinking**
    to re-evaluate reasoning, reorganize the plan, and attempt a more structured approach.

- When confidence in your current plan is low, or when uncertainty or ambiguity is detected
    in the user request, switch to **Sequential Thinking** before proceeding.

- For tasks with multiple interdependent steps (three or more), always begin in **Sequential Thinking** mode
    to maintain clarity and logical consistency between stages.

- If the same type of error or confusion repeats (e.g., logic loop, parsing issue, or unclear intent),
    engage **Sequential Thinking** to isolate the root cause and adjust your strategy.

- When the user explicitly expresses dissatisfaction (e.g., “no”, “not correct”, “wrong direction”, “try again”),
    activate **Sequential Thinking** before producing your next output.

- Always summarize the insights gained from **Sequential Thinking** at the end of the process,
    highlighting what changed in your reasoning or plan.
- DON'T ADD MARKDOWN FILES TO APP ROOT ... DON'T CREATE MARKUP FILES WITHOUT ASKING THE USER
