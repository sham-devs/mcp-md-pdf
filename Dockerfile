# Dockerfile for md-pdf-mcp
# Provides DOCX and PDF conversion (using LibreOffice for PDF)

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including LibreOffice for PDF conversion
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY README.md .
COPY src/ src/

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Expose MCP server on stdio
# The MCP server communicates via standard input/output
CMD ["python", "-m", "md_pdf_mcp.server"]

# Build instructions:
# docker build -t md-pdf-mcp .
#
# Run instructions:
# docker run -i md-pdf-mcp
#
# Features:
# - Markdown to DOCX conversion (python-docx)
# - DOCX to PDF conversion (LibreOffice headless mode)
# - Full cross-platform support
