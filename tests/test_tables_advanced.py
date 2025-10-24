"""
Tests for advanced table scenarios

Tests cover:
- Empty tables
- Tables with empty cells
- Single row/column tables
- Tables with special formatting
- Malformed tables
"""
import os
import pytest
from docx import Document
from src.md_pdf_mcp.converter import MarkdownConverter


class TestTableEdgeCases:
    """Test table edge cases and special scenarios"""

    def test_empty_table(self, output_docx_path, temp_dir):
        """Test table with no data rows"""
        md = os.path.join(temp_dir, "empty_table.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Empty Table\n\n")
            f.write("| Header 1 | Header 2 |\n")
            f.write("|----------|----------|\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True

    def test_table_with_empty_cells(self, output_docx_path, temp_dir):
        """Test table with empty cells"""
        md = os.path.join(temp_dir, "empty_cells.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Table with Empty Cells\n\n")
            f.write("| Header 1 | Header 2 | Header 3 |\n")
            f.write("|----------|----------|----------|\n")
            f.write("| Data 1   |          | Data 3   |\n")
            f.write("|          | Data 2   |          |\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True
        assert os.path.exists(output_docx_path)

    def test_single_column_table(self, output_docx_path, temp_dir):
        """Test table with only one column"""
        md = os.path.join(temp_dir, "single_col.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Single Column Table\n\n")
            f.write("| Header |\n")
            f.write("|--------|\n")
            f.write("| Row 1  |\n")
            f.write("| Row 2  |\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True

    def test_single_row_table(self, output_docx_path, temp_dir):
        """Test table with only header row"""
        md = os.path.join(temp_dir, "single_row.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Single Row Table\n\n")
            f.write("| Col1 | Col2 | Col3 |\n")
            f.write("|------|------|------|\n")
            f.write("| Data | Data | Data |\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True

    def test_table_with_formatting_in_cells(self, output_docx_path, temp_dir):
        """Test table cells with bold, italic, code"""
        md = os.path.join(temp_dir, "formatted_table.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Formatted Table\n\n")
            f.write("| Bold      | Italic    | Code      |\n")
            f.write("|-----------|-----------|--------|\n")
            f.write("| **bold**  | *italic*  | `code` |\n")
            f.write("| **B1**    | *I1*      | `C1`   |\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True
        assert os.path.exists(output_docx_path)

    def test_table_with_line_breaks_in_cells(self, output_docx_path, temp_dir):
        """Test table cells with line breaks"""
        md = os.path.join(temp_dir, "linebreak_table.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Table with Line Breaks\n\n")
            f.write("| Header 1 | Header 2 |\n")
            f.write("|----------|----------|\n")
            f.write("| Line 1<br>Line 2 | Data |\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        # Should complete (line breaks may not render perfectly)
        assert result is True

    def test_malformed_table_missing_pipes(self, output_docx_path, temp_dir):
        """Test table with missing pipes"""
        md = os.path.join(temp_dir, "malformed.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Malformed Table\n\n")
            f.write("| Header 1 | Header 2 |\n")
            f.write("|----------|----------|  \n")
            f.write("Data 1 | Data 2\n")  # Missing leading pipe
            f.write("| Data 3 Data 4 |\n")  # Missing middle pipe

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        # Should handle gracefully
        assert result is True

    def test_table_with_inconsistent_columns(self, output_docx_path, temp_dir):
        """Test table where rows have different column counts"""
        md = os.path.join(temp_dir, "inconsistent.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Inconsistent Columns\n\n")
            f.write("| H1 | H2 | H3 |\n")
            f.write("|----|----|----|\n")
            f.write("| D1 | D2 |\n")  # Only 2 columns
            f.write("| D1 | D2 | D3 | D4 |\n")  # 4 columns

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        # Should handle gracefully (may pad/truncate)
        assert result is True

    def test_table_with_unicode_in_cells(self, output_docx_path, temp_dir):
        """Test table with various Unicode characters"""
        md = os.path.join(temp_dir, "unicode_table.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Unicode Table\n\n")
            f.write("| Emoji | CJK | RTL |\n")
            f.write("|-------|-----|-----|\n")
            f.write("| 😀 ✅ 🔥 | 你好 | مرحبا |\n")
            f.write("| 🎉 ❤️ ⚡ | 世界 | שלום |\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True

    def test_table_with_very_long_cell_content(self, output_docx_path, temp_dir):
        """Test table cell with extremely long text"""
        md = os.path.join(temp_dir, "long_cell.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Long Cell Content\n\n")
            f.write("| Header 1 | Header 2 |\n")
            f.write("|----------|----------|\n")

            # 500 word cell
            long_text = " ".join(["word"] * 500)
            f.write(f"| {long_text} | Normal |\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True

    def test_nested_tables_not_supported(self, output_docx_path, temp_dir):
        """Test that nested tables are handled (not truly nested in Word)"""
        md = os.path.join(temp_dir, "nested.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Nested Tables\n\n")
            f.write("| Outer |\n")
            f.write("|-------|\n")
            f.write("| | Inner | |\n")
            f.write("| |---|---| |\n")
            f.write("| | A | B | |\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        # Should complete (may not render as expected)
        assert result is True

    def test_table_with_alignment_markers(self, output_docx_path, temp_dir):
        """Test table with column alignment markers"""
        md = os.path.join(temp_dir, "aligned.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Aligned Table\n\n")
            f.write("| Left | Center | Right |\n")
            f.write("|:-----|:------:|------:|\n")
            f.write("| L1   | C1     | R1    |\n")
            f.write("| L2   | C2     | R2    |\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        # Should complete (alignment may not be applied)
        assert result is True
