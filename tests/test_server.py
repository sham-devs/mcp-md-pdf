"""
Tests for FastMCP server tools

Tests cover:
- convert_markdown tool
- convert_markdown_batch tool
- list_supported_formats tool
- Error handling and validation
"""
import os
import pytest
from src.md_pdf_mcp import server

# Use the internal implementations for testing
convert_markdown = server._convert_markdown_impl
convert_markdown_batch = server.convert_markdown_batch.fn
list_supported_formats = server.list_supported_formats.fn


class TestConvertMarkdownTool:
    """Test the convert_markdown MCP tool"""

    def test_convert_to_docx(self, simple_markdown, temp_dir):
        """Test converting to DOCX format"""
        output_path = os.path.join(temp_dir, "output")

        result = convert_markdown(
            markdown_path=simple_markdown,
            output_path=output_path,
            output_format="docx"
        )

        assert "✓ Created:" in result
        assert "output.docx" in result
        assert os.path.exists(f"{output_path}.docx")

    @pytest.mark.slow
    def test_convert_to_both(self, simple_markdown, temp_dir):
        """Test converting to both DOCX and PDF"""
        output_path = os.path.join(temp_dir, "output")

        result = convert_markdown(
            markdown_path=simple_markdown,
            output_path=output_path,
            output_format="both"
        )

        assert "output.docx" in result

        # PDF might fail if Word not installed
        if "✓ Created:" in result and "pdf" in result:
            assert os.path.exists(f"{output_path}.pdf")

    def test_nonexistent_markdown(self, temp_dir):
        """Test error handling for nonexistent markdown file"""
        output_path = os.path.join(temp_dir, "output")

        result = convert_markdown(
            markdown_path="nonexistent.md",
            output_path=output_path,
            output_format="docx"
        )

        assert "❌ Error:" in result
        assert "not found" in result

    def test_nonexistent_template(self, simple_markdown, temp_dir):
        """Test error handling for nonexistent template"""
        output_path = os.path.join(temp_dir, "output")

        result = convert_markdown(
            markdown_path=simple_markdown,
            output_path=output_path,
            output_format="docx",
            template_path="nonexistent.dotx"
        )

        assert "❌ Error:" in result
        assert "Template file not found" in result

    def test_output_directory_creation(self, simple_markdown, temp_dir):
        """Test that output directory is created if needed"""
        output_path = os.path.join(temp_dir, "new_dir", "output")

        result = convert_markdown(
            markdown_path=simple_markdown,
            output_path=output_path,
            output_format="docx"
        )

        assert "✓ Created:" in result
        assert os.path.exists(f"{output_path}.docx")

    def test_pdf_only_output(self, simple_markdown, temp_dir):
        """Test PDF-only output (should create temp DOCX and delete it)"""
        output_path = os.path.join(temp_dir, "output")

        result = convert_markdown(
            markdown_path=simple_markdown,
            output_path=output_path,
            output_format="pdf"
        )

        # Temp DOCX should be deleted
        assert not os.path.exists(f"{output_path}_temp.docx")

        # Result should indicate PDF creation attempt
        assert "pdf" in result.lower()


class TestConvertMarkdownBatchTool:
    """Test the convert_markdown_batch MCP tool"""

    def test_batch_conversion_success(self, temp_dir):
        """Test successful batch conversion of multiple files"""
        # Create multiple markdown files
        md_files = []
        for i in range(3):
            md_path = os.path.join(temp_dir, f"test{i}.md")
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(f"# Test Document {i}\n\nContent for file {i}")
            md_files.append(md_path)

        output_dir = os.path.join(temp_dir, "output")

        result = convert_markdown_batch(
            markdown_files=md_files,
            output_dir=output_dir,
            output_format="docx"
        )

        assert "Batch Conversion Complete" in result
        assert "Success: 3" in result

        # Check that output files exist
        for i in range(3):
            assert os.path.exists(os.path.join(output_dir, f"test{i}.docx"))

    def test_batch_with_missing_files(self, simple_markdown, temp_dir):
        """Test batch conversion with some missing files"""
        md_files = [
            simple_markdown,
            "nonexistent1.md",
            "nonexistent2.md"
        ]

        output_dir = os.path.join(temp_dir, "output")

        result = convert_markdown_batch(
            markdown_files=md_files,
            output_dir=output_dir,
            output_format="docx"
        )

        assert "Success: 1" in result
        assert "Failed: 2" in result
        assert "Skipped (not found)" in result

    def test_batch_with_nonexistent_template(self, temp_dir):
        """Test batch conversion with nonexistent template"""
        md_path = os.path.join(temp_dir, "test.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write("# Test\n\nContent")

        output_dir = os.path.join(temp_dir, "output")

        result = convert_markdown_batch(
            markdown_files=[md_path],
            output_dir=output_dir,
            output_format="docx",
            template_path="nonexistent.dotx"
        )

        assert "❌ Error:" in result
        assert "Template file not found" in result

    def test_empty_batch(self, temp_dir):
        """Test batch conversion with empty file list"""
        output_dir = os.path.join(temp_dir, "output")

        result = convert_markdown_batch(
            markdown_files=[],
            output_dir=output_dir,
            output_format="docx"
        )

        assert "Success: 0" in result
        assert "Failed: 0" in result


class TestListSupportedFormatsTool:
    """Test the list_supported_formats MCP tool"""

    def test_list_formats_returns_info(self):
        """Test that list_supported_formats returns format information"""
        result = list_supported_formats()

        assert "MD-PDF-MCP Converter" in result
        assert "INPUT FORMATS" in result
        assert "OUTPUT FORMATS" in result
        assert "FEATURES" in result
        assert ".md" in result
        assert ".docx" in result
        assert ".pdf" in result

    def test_list_formats_mentions_features(self):
        """Test that key features are mentioned"""
        result = list_supported_formats()

        assert "template" in result.lower()
        assert "bullet" in result.lower() or "list" in result.lower()
        assert "batch" in result.lower()

    def test_list_formats_mentions_platform_notes(self):
        """Test that platform-specific notes are included"""
        result = list_supported_formats()

        assert "PLATFORM" in result or "Windows" in result
        assert "Word" in result or "MS Word" in result
