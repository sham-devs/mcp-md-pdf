"""
Pytest configuration and shared fixtures for mcp-md-pdf tests
"""
import os
import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test outputs"""
    temp_path = tempfile.mkdtemp(prefix="md_pdf_test_")
    yield temp_path
    # Cleanup after test
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_markdown(temp_dir):
    """Create a sample markdown file for testing"""
    md_content = """# Test Document

This is a test document for the mcp-md-pdf converter.

## Features Tested

### Headings
This tests H1, H2, and H3 headings.

#### H4 Heading
Testing H4 support.

##### H5 Heading
Testing H5 support.

###### H6 Heading
Testing H6 support.

### Text Formatting
This paragraph has **bold text**, *italic text*, and `inline code`.

### Lists

#### Bullet Lists
- First bullet point
- Second bullet point
- Third bullet point with **bold**

#### Numbered Lists
1. First numbered item
2. Second numbered item
3. Third numbered item

### Code Blocks
```python
def hello_world():
    print("Hello, World!")
```

### Blockquotes
> This is a blockquote.
> It can span multiple lines.

### Tables
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | **Bold** | *Italic* |
| Data 2   | `Code`   | Normal   |

### Horizontal Rule
---

## Conclusion
This covers the main markdown features.
"""
    md_path = os.path.join(temp_dir, "sample.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    return md_path


@pytest.fixture
def simple_markdown(temp_dir):
    """Create a simple markdown file for basic tests"""
    md_content = """# Simple Test

This is a simple test document.

- Bullet 1
- Bullet 2

1. Number 1
2. Number 2
"""
    md_path = os.path.join(temp_dir, "simple.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    return md_path


@pytest.fixture
def markdown_with_emoji(temp_dir):
    """Create markdown with emoji and special characters"""
    md_content = """# User Requirements

## Overview

This document includes emoji:

- ✅ Understanding ZATCA
- ✅ All required fields
- ✅ Code examples

## Unicode Support
Testing unicode: 你好世界 مرحبا بالعالم
"""
    md_path = os.path.join(temp_dir, "emoji.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    return md_path


@pytest.fixture
def output_docx_path(temp_dir):
    """Generate output path for DOCX files"""
    return os.path.join(temp_dir, "output.docx")


@pytest.fixture
def output_pdf_path(temp_dir):
    """Generate output path for PDF files"""
    return os.path.join(temp_dir, "output.pdf")
