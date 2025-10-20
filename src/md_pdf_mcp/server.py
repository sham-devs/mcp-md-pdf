#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastMCP Server for Markdown to Word/PDF Conversion

Exposes tools for converting markdown files to Word and PDF formats
with optional .dotx template support.
"""

import os
from pathlib import Path
from typing import Optional, Literal
from fastmcp import FastMCP

from .converter import MarkdownConverter

# Create FastMCP server instance
mcp = FastMCP("md-pdf-converter")

# Initialize converter
converter = MarkdownConverter()


def _convert_markdown_impl(
    markdown_path: str,
    output_path: str,
    output_format: Literal["docx", "pdf", "both"] = "docx",
    template_path: Optional[str] = None
) -> str:
    """
    Internal implementation for markdown conversion.
    Used by both convert_markdown tool and convert_markdown_batch.
    """
    try:
        # Validate inputs
        if not os.path.exists(markdown_path):
            return f"❌ Error: Markdown file not found: {markdown_path}"

        if template_path and not os.path.exists(template_path):
            return f"❌ Error: Template file not found: {template_path}"

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path) or "."
        os.makedirs(output_dir, exist_ok=True)

        results = []

        # Create DOCX (always needed, even for PDF-only)
        docx_path = f"{output_path}.docx"
        temp_docx = None

        if output_format == "pdf":
            # For PDF-only, use temp file
            temp_docx = f"{output_path}_temp.docx"
            converter.markdown_to_word(markdown_path, temp_docx, template_path)
            docx_for_pdf = temp_docx
        else:
            # For docx or both, create final docx
            converter.markdown_to_word(markdown_path, docx_path, template_path)
            docx_for_pdf = docx_path
            results.append(f"✓ Created: {docx_path}")

        # Create PDF if requested
        if output_format in ["pdf", "both"]:
            pdf_path = f"{output_path}.pdf"
            try:
                converter.word_to_pdf(docx_for_pdf, pdf_path)
                results.append(f"✓ Created: {pdf_path}")
            except Exception as e:
                results.append(f"❌ PDF conversion failed: {str(e)}")
                results.append("💡 Tip: PDF conversion requires Microsoft Word on Windows")

            # Clean up temp file
            if temp_docx and os.path.exists(temp_docx):
                os.remove(temp_docx)

        return "\n".join(results)

    except Exception as e:
        return f"❌ Conversion failed: {str(e)}"


@mcp.tool()
def convert_markdown(
    markdown_path: str,
    output_path: str,
    output_format: Literal["docx", "pdf", "both"] = "docx",
    template_path: Optional[str] = None
) -> str:
    """
    Convert markdown to Word/PDF with optional .dotx template.

    This tool converts markdown files to professional documents using python-docx.
    You can optionally provide a .dotx template file for consistent styling.

    Args:
        markdown_path: Path to input .md file
        output_path: Base path for output (without extension)
        output_format: Output format - "docx" (Word), "pdf", or "both"
        template_path: Optional path to .dotx template file for styling

    Returns:
        Success message with created file paths

    Examples:
        convert_markdown("README.md", "output", "docx")
        → Creates output.docx

        convert_markdown("doc.md", "result", "pdf", "template.dotx")
        → Creates result.pdf with template styling

        convert_markdown("guide.md", "final", "both", "company.dotx")
        → Creates final.docx and final.pdf with company template
    """
    return _convert_markdown_impl(markdown_path, output_path, output_format, template_path)


@mcp.tool()
def convert_markdown_batch(
    markdown_files: list[str],
    output_dir: str,
    output_format: Literal["docx", "pdf", "both"] = "docx",
    template_path: Optional[str] = None
) -> str:
    """
    Batch convert multiple markdown files to Word/PDF.

    Converts a list of markdown files using the same template and format settings.
    Output files are named after input files and placed in the specified directory.

    Args:
        markdown_files: List of paths to .md files
        output_dir: Directory for output files
        output_format: Output format for all files - "docx", "pdf", or "both"
        template_path: Optional shared template for all conversions

    Returns:
        Summary of conversions with success/failure counts

    Example:
        convert_markdown_batch(
            ["doc1.md", "doc2.md", "doc3.md"],
            "output",
            "both",
            "template.dotx"
        )
        → Converts all 3 files to output/ with template styling
    """
    try:
        # Validate output directory
        os.makedirs(output_dir, exist_ok=True)

        if template_path and not os.path.exists(template_path):
            return f"❌ Error: Template file not found: {template_path}"

        results = []
        success_count = 0
        fail_count = 0

        for md_file in markdown_files:
            if not os.path.exists(md_file):
                results.append(f"⊘ Skipped (not found): {md_file}")
                fail_count += 1
                continue

            # Generate output path from input filename
            base_name = Path(md_file).stem
            output_path = os.path.join(output_dir, base_name)

            # Convert using internal implementation
            result = _convert_markdown_impl(md_file, output_path, output_format, template_path)

            if "✓" in result:
                success_count += 1
                results.append(f"✓ {base_name}")
            else:
                fail_count += 1
                results.append(f"❌ {base_name}: {result}")

        # Summary
        summary = f"\n{'='*50}\nBatch Conversion Complete\n{'='*50}\n"
        summary += f"✓ Success: {success_count}\n"
        summary += f"❌ Failed: {fail_count}\n"
        summary += f"{'='*50}\n\n"

        return summary + "\n".join(results)

    except Exception as e:
        return f"❌ Batch conversion failed: {str(e)}"


@mcp.tool()
def list_supported_formats() -> str:
    """
    List all supported input/output formats and features.

    Returns:
        Information about supported formats and features
    """
    return """
📄 MD-PDF-MCP Converter - Supported Formats

INPUT FORMATS:
✓ Markdown (.md) - Full GitHub Flavored Markdown support
  - Headings (H1, H2, H3)
  - Bold, italic, code inline formatting
  - Bullet lists (nested up to 3 levels)
  - Numbered lists
  - Code blocks
  - Blockquotes

OUTPUT FORMATS:
✓ Word (.docx) - Microsoft Word format
✓ PDF (.pdf) - Portable Document Format (requires MS Word on Windows)

FEATURES:
✓ Optional .dotx template support for custom styling
✓ Automatic bullet/numbering formatting
✓ Code syntax highlighting preservation
✓ Nested list support
✓ Batch conversion of multiple files
✓ Cross-platform (except PDF conversion)

TEMPLATE SUPPORT:
✓ Microsoft Word templates (.dotx)
✓ Custom heading styles
✓ Custom fonts and colors
✓ Page layouts and margins
✓ Headers and footers

PLATFORM NOTES:
• DOCX conversion: Works on all platforms (Windows, Mac, Linux)
• PDF conversion: Requires Microsoft Word (Windows only via COM)
  Alternative: Use LibreOffice or other PDF converter after creating DOCX
"""


def main():
    """Entry point for the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()
