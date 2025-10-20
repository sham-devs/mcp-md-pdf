# **MD-PDF-MCP: Markdown to Word/PDF Converter**

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

### Option 1: Using `uvx` (Recommended)

```bash
# Install and run with uvx
uvx md-pdf-mcp
```

### Option 2: From Source

```bash
# Clone or navigate to the repository
cd md-pdf-mcp

# Install in development mode
pip install -e .

# Or install from PyPI (when published)
pip install md-pdf-mcp
```

### Option 3: Using Docker

```bash
# Build the Docker image
docker build -t md-pdf-mcp .

# Run with Docker
docker run -i md-pdf-mcp

# Or use docker-compose
docker-compose up -d
```

**Note:** Docker container supports **both DOCX and PDF conversion**. PDF conversion uses LibreOffice in headless mode.

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

Open the configuration file and add the md-pdf-mcp server:

**Option A: Using uvx (Recommended)**
```json
{
  "mcpServers": {
    "md-pdf": {
      "command": "uvx",
      "args": ["md-pdf-mcp"]
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
        "PYTHONPATH": "/path/to/md-pdf-mcp"
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

## **Platform Notes**

* **DOCX Conversion:** Works on all platforms (Windows, macOS, Linux)
* **PDF Conversion:** Cross-platform support with automatic detection
  - **Windows:** Uses Microsoft Word via COM automation (requires MS Word installed)
  - **macOS/Linux:** Uses LibreOffice in headless mode (requires LibreOffice installed)
  - **Docker:** Includes LibreOffice for PDF conversion

**Installation Requirements:**

**Windows:**
```bash
pip install pywin32  # For MS Word integration
```

**macOS:**
```bash
brew install --cask libreoffice
```

**Ubuntu/Debian:**
```bash
sudo apt-get install libreoffice libreoffice-writer
```

**Fedora:**
```bash
sudo dnf install libreoffice
```

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
git clone https://github.com/yourusername/md-pdf-mcp.git
cd md-pdf-mcp

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
* Or install from PyPI: `pip install md-pdf-mcp`

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
