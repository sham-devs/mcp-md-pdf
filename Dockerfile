# Dockerfile for md-pdf-mcp
# Provides DOCX conversion (PDF requires Windows + MS Word, not available in Linux containers)

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
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
# Note: PDF conversion is not available in Docker (requires Windows + Microsoft Word)
# This container supports Markdown to DOCX conversion only.
