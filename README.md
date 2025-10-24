# **MCP-MD-PDF: Markdown to Word/PDF Converter**

[![PyPI version](https://img.shields.io/pypi/v/mcp-md-pdf.svg)](https://pypi.org/project/mcp-md-pdf/)
[![Python Versions](https://img.shields.io/pypi/pyversions/mcp-md-pdf.svg)](https://pypi.org/project/mcp-md-pdf/)
[![Tests](https://github.com/sham-devs/mcp-md-pdf/actions/workflows/tests.yml/badge.svg)](https://github.com/sham-devs/mcp-md-pdf/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple, reliable Model Context Protocol (MCP) server that converts Markdown files into professional Word (.docx) and PDF documents — with full support for `.dotx` templates.

---

## **Background**

This tool was born from a practical need.
We often write documentation, guides, and technical notes in Markdown — it’s fast, lightweight, and easy to version.
But when it’s time to deliver these files to clients or present them professionally, we usually want them to match our project or company style: clean layout, consistent fonts, branded cover page, and polished formatting.

So instead of doing that manually every time, we built a simple flow:

> Convert Markdown → Word (.docx using a `.dotx` template) → PDF

By using Word templates, we could apply our own design once and keep every document consistent.
That’s where this small project came from — a quick way to turn Markdown into beautiful, ready-to-share documents that look like they belong to your organization.

---

## **Features**

* 🚀 **Fast Conversion** – From Markdown to Word or PDF in seconds
* 🎨 **Template Support** – Apply `.dotx` templates for consistent, branded styling
* 📦 **Batch Processing** – Convert multiple files at once
* 🔧 **Flexible Output** – Choose between `.docx`, `.pdf`, or both
* 🤖 **AI-Ready** – Built to integrate smoothly with Claude and other MCP-compatible AI tools

---

## **Installation**

Choose the installation method that best fits your needs:

| Method | Code Download? | PDF Support | Best For |
|--------|---------------|-------------|----------|
| **uvx** (Option 1) | ❌ No | ✅ Yes (LibreOffice required) | Claude Desktop users |
| **pip** (Option 2) | ❌ No | ✅ Yes (LibreOffice required) | Python package users |
| **From Source** (Option 3) | ✅ Yes | ✅ Yes (LibreOffice required) | Developers |

### Option 1: Using `uvx` (Recommended - No Code Download Needed)

**Best for:** Claude Desktop users who want the simplest installation.

**Requirements:**
- Python 3.10+
- For PDF conversion:
  - **Windows:** Microsoft Word (uses COM automation)
  - **macOS:** LibreOffice (`brew install --cask libreoffice`)
  - **Linux:** LibreOffice (`sudo apt-get install libreoffice`)

**Installation:**
```bash
# No code download needed - uvx handles everything
uvx mcp-md-pdf
```

**Claude Desktop Setup:**

Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "md-pdf": {
      "command": "uvx",
      "args": ["mcp-md-pdf"]
    }
  }
}
```

**Restart Claude Desktop** for changes to take effect.

> 📖 See [Configuration section](#configuration) for config file location and alternative setups.

---

### Option 2: Using `pip` (No Code Download Needed)

**Best for:** Users who want to install as a Python package.

**Requirements:**
- Python 3.10+
- For PDF conversion (same as Option 1):
  - **Windows:** Microsoft Word
  - **macOS/Linux:** LibreOffice

**Installation:**
```bash
# Install from PyPI (when published)
pip install mcp-md-pdf

# Or install with development dependencies
pip install "mcp-md-pdf[dev]"
```

**Claude Desktop Setup:**

Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "md-pdf": {
      "command": "python",
      "args": ["-m", "md_pdf_mcp.server"]
    }
  }
}
```

**Restart Claude Desktop** for changes to take effect.

> 📖 See [Configuration section](#configuration) for config file location and alternative setups.

---

### Option 3: From Source (Code Download Required)

**Best for:** Developers who want to modify the code or contribute.

**Requirements:**
- Git
- Python 3.10+
- For PDF conversion (same as above)

**Installation:**
```bash
# Step 1: Clone the repository
git clone https://github.com/sham-devs/mcp-md-pdf.git
cd mcp-md-pdf

# Step 2: Install in development mode
pip install -e .

# Step 3: (Optional) Install dev dependencies
pip install -e ".[dev]"
```

**Claude Desktop Setup:**

Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "md-pdf": {
      "command": "python",
      "args": ["-m", "md_pdf_mcp.server"]
    }
  }
}
```

**Restart Claude Desktop** for changes to take effect.

> 📖 See [Configuration section](#configuration) for config file location and alternative setups.

---

## **Configuration**

### Step 1: Find Your Configuration File

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Step 2: Add MCP Server

Open the configuration file and add the mcp-md-pdf server:

**Option A: Using uvx (Recommended)**
```json
{
  "mcpServers": {
    "md-pdf": {
      "command": "uvx",
      "args": ["mcp-md-pdf"]
    }
  }
}
```

**Option B: Local Installation**
```json
{
  "mcpServers": {
    "md-pdf": {
      "command": "python",
      "args": ["-m", "md_pdf_mcp.server"]
    }
  }
}
```

**Option C: With Environment Variables**
```json
{
  "mcpServers": {
    "md-pdf": {
      "command": "python",
      "args": ["-m", "md_pdf_mcp.server"],
      "env": {
        "PYTHONPATH": "/path/to/mcp-md-pdf"
      }
    }
  }
}
```

### Step 3: Restart Claude Desktop

Close and reopen Claude Desktop for changes to take effect.

---

## **Usage**

### With Claude Desktop

After setup, restart Claude Desktop and simply ask:

```
Convert my README.md to Word format

Convert docs.md to PDF using my company-template.dotx

Convert all markdown files in the docs folder to both Word and PDF
```

---

## **MCP Tools**

### 1. `convert_markdown`

Convert a single Markdown file to Word or PDF.

**Parameters:**

* `markdown_path` *(str)* – Path to the `.md` file
* `output_path` *(str)* – Output base path (no extension)
* `output_format` *(str)* – `"docx"`, `"pdf"`, or `"both"` (default: `"docx"`)
* `template_path` *(str, optional)* – Path to `.dotx` template

**Examples:**

```python
# Create Word document
convert_markdown("README.md", "output", "docx")

# Create PDF with template
convert_markdown("doc.md", "result", "pdf", "template.dotx")

# Create both formats
convert_markdown("guide.md", "final", "both", "company.dotx")
```

---

### 2. `convert_markdown_batch`

Convert multiple Markdown files at once.

**Parameters:**

* `markdown_files` *(list[str])* – List of `.md` files
* `output_dir` *(str)* – Output directory
* `output_format` *(str)* – `"docx"`, `"pdf"`, or `"both"`
* `template_path` *(str, optional)* – Shared `.dotx` template

**Example:**

```python
convert_markdown_batch(
  ["doc1.md", "doc2.md", "doc3.md"],
  "output",
  "both",
  "template.dotx"
)
```

---

### 3. `list_supported_formats`

List supported formats and their capabilities.

---

## **Supported Markdown Features**

| Feature                 | Supported | Notes                                                |
| ----------------------- | --------- | ---------------------------------------------------- |
| Headings (H1–H6)        | ✅         | `#` through `######`, with template fallback         |
| **Bold** / *Italic*     | ✅         | Markdown standard syntax                             |
| Inline code             | ✅         | Monospaced with gray background                      |
| Code blocks             | ✅         | Professional styling with background and borders     |
| Bullet & Numbered lists | ✅         | Nested up to 3 levels                                |
| Tables                  | ✅         | With header styling and inline formatting            |
| Blockquotes             | ✅         | Italic text with left border and background shading  |
| Horizontal rules        | ✅         | `---`                                                |
| Unicode & Emoji         | ✅         | Full UTF-8 support                                   |

**For detailed feature coverage analysis, see [docs/MARKDOWN_COVERAGE.md](docs/MARKDOWN_COVERAGE.md)**

---

## **Template Support**

Use a `.dotx` Word template to define your document style:

* Custom headings, fonts, and colors
* Page margins and layout
* Headers and footers
* Branding and logo placement
* Table of contents formatting

If no template is provided, a clean default design is used.

---

## **PDF Conversion Setup**

**Important:** PDF conversion requires LibreOffice (or Microsoft Word on Windows) to preserve all DOCX formatting.

### Why LibreOffice?

LibreOffice is **required** for PDF conversion because it preserves ALL formatting from DOCX files:
- ✅ **Colors, backgrounds, borders** - Professional styling intact
- ✅ **Code blocks** - Syntax highlighting and backgrounds preserved
- ✅ **Tables** - Headers, borders, and cell styling maintained
- ✅ **Template styles** - `.dotx` template formatting carried through to PDF
- ✅ **Fonts & spacing** - Typography remains pixel-perfect

**Alternative approaches (Pandoc, etc.) lose formatting** - they treat DOCX as plain text markup, stripping visual styles during PDF conversion.

---

### DOCX Conversion (All Platforms)
✅ Works out of the box - no additional software needed!

### PDF Conversion (Platform-Specific)

#### Windows Users

**Option A: Microsoft Word (Best for Windows)**

If you have Microsoft Word installed:
```bash
# Install Python COM automation library
pip install pywin32
```

That's it! The converter will automatically use Word for PDF conversion.

**Option B: LibreOffice (Recommended if no Word)**
```bash
# Method 1: Direct download (easiest)
# Visit: https://www.libreoffice.org/download/

# Method 2: Using Chocolatey package manager
choco install libreoffice

# Method 3: Using winget (Windows Package Manager)
winget install TheDocumentFoundation.LibreOffice
```

**Verify installation:**
```powershell
# Check if LibreOffice is installed
where.exe soffice
# Should output: C:\Program Files\LibreOffice\program\soffice.exe
```

---

#### macOS Users

**LibreOffice is REQUIRED for PDF conversion on macOS** (no native MS Word COM support).

**Installation (Choose one method):**

```bash
# Method 1: Homebrew (RECOMMENDED - easiest updates)
brew install --cask libreoffice

# Method 2: Direct download
# Visit: https://www.libreoffice.org/download/
# Download LibreOffice_25.x.x_MacOS_aarch64.dmg (M1/M2/M3)
# Or LibreOffice_25.x.x_MacOS_x86-64.dmg (Intel Macs)
```

**System Requirements:**
- macOS 10.15 (Catalina) or newer
- ~800 MB disk space
- Works on both Intel and Apple Silicon (M1/M2/M3)

**Verify installation:**
```bash
which soffice
# Should output: /Applications/LibreOffice.app/Contents/MacOS/soffice

libreoffice --version
# Should output: LibreOffice 25.x.x or higher
```

---

#### Linux Users

**Ubuntu/Debian (Recommended method):**
```bash
# Update package list
sudo apt-get update

# Install LibreOffice (headless mode supported)
sudo apt-get install -y libreoffice libreoffice-writer

# Optional: Install additional fonts for better compatibility
sudo apt-get install -y fonts-liberation fonts-dejavu
```

**For headless servers (CI/CD):**
```bash
# Minimal installation without GUI components
sudo apt-get install -y libreoffice-writer libreoffice-calc \
  libxinerama1 libfontconfig1 libdbus-glib-1-2 libcairo2 \
  libcups2 libglu1-mesa libsm6
```

**Fedora/RHEL:**
```bash
sudo dnf install libreoffice libreoffice-writer
```

**Arch Linux:**
```bash
sudo pacman -S libreoffice-fresh
```

**Verify installation:**
```bash
libreoffice --version
# Should output: LibreOffice 7.x or 25.x

# Test headless mode
soffice --headless --version
# Should output version without GUI
```

---

## **Platform Notes**

* **DOCX Conversion:** Works on all platforms (Windows, macOS, Linux) - **no additional software required**
* **PDF Conversion:** Cross-platform with automatic platform detection:
  - **Windows:** Uses Microsoft Word (if installed) or LibreOffice
  - **macOS/Linux:** Uses LibreOffice in headless mode

**Why LibreOffice for PDF?** LibreOffice preserves **ALL** DOCX formatting when converting to PDF:
- ✅ Colors, backgrounds, and borders
- ✅ Professional code block styling (#F5F5F5 backgrounds)
- ✅ Blockquote borders (blue left border)
- ✅ Table headers with colored backgrounds
- ✅ Template styles from .dotx files
- ✅ Fonts, spacing, and layout

---

## **Requirements**

* Python 3.10+
* `Pillow` (image handling)
* `python-docx` (Word generation)
* `pywin32` (Windows only)
* `fastmcp` (MCP framework)

---

## **Development**

```bash
# Clone the repository
git clone https://github.com/sham-devs/mcp-md-pdf.git
cd mcp-md-pdf

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=src/md_pdf_mcp --cov-report=html

# Format code
black src/ tests/
ruff check src/ tests/
```

---

## **Testing**

Covers:

* Markdown → Word conversion
* Template application
* MCP server tools
* Unicode, emoji, and edge cases

**Structure:**

```
tests/
├── conftest.py
├── test_converter.py
├── test_server.py
└── README.md
```

---

## **Examples**

```bash
# Run the MCP server directly
python -m md_pdf_mcp.server
```

Or inspect via:

```bash
npx @modelcontextprotocol/inspector python -m md_pdf_mcp.server
```

**Example usage:**

```
User: Convert my README.md to Word format
→ Created: README.docx

User: Create a PDF with our company template
→ Created: guide.pdf

User: Convert all docs to both formats
→ Batch Conversion Complete (5 succeeded, 0 failed)
```

---

## **Troubleshooting**

### Server Not Showing Up in Claude Desktop

1. Verify `claude_desktop_config.json` is valid JSON (no trailing commas)
2. Check that the Python path is correct for your system
3. Review Claude Desktop logs:
   - **Windows:** `%APPDATA%\Claude\logs\`
   - **macOS:** `~/Library/Logs/Claude/`
4. Restart Claude Desktop completely

### Python Path Issues

Verify your Python installation:

```bash
python --version
# or
python3 --version
```

If the command doesn't work, find your Python path:
- **Windows:** `where python`
- **macOS/Linux:** `which python3`

Update the configuration file with the correct path.

### PDF Conversion Fails

**Error:** `pywin32 library required for PDF conversion on Windows`

**Fix (Windows):**
```bash
pip install pywin32
```

**Error:** `LibreOffice not found`

**Fix (macOS):**
```bash
brew install --cask libreoffice
```

**Fix (Ubuntu/Debian):**
```bash
sudo apt-get install libreoffice libreoffice-writer
```

**Fix (Fedora):**
```bash
sudo dnf install libreoffice
```

### Template Not Loading

**Error:** Invalid or missing `.dotx` file

**Fix:**
* Verify the file path and extension are correct
* Ensure the template file exists and is accessible
* Try conversion without template to isolate the issue

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'fastmcp'`

**Fix:**
* Run `pip install -e .` from the project directory
* Or install from PyPI: `pip install mcp-md-pdf`

### Testing with MCP Inspector

For advanced debugging, test the server directly:

```bash
npx @modelcontextprotocol/inspector python -m md_pdf_mcp.server
```

This opens a web interface to interact with the MCP tools directly.

---

## **License**

MIT License – see `LICENSE` file.

---

## **Contributing**

Pull requests are welcome.
If you have ideas for improving conversions, templates, or new formats, we’d love to see them.

---

## **Credits**

Built with ❤️ using the FastMCP framework —
created to make Markdown documents look like real reports, not just text on GitHub.
