"""
Tests for advanced markdown features

Tests cover:
- Strikethrough
- Task lists
- HTML entities
- Escape sequences
- Nested formatting
- Links and images
"""
import os
import pytest
from src.md_pdf_mcp.converter import MarkdownConverter


class TestTextFormattingAdvanced:
    """Test advanced text formatting"""

    def test_strikethrough_text(self, output_docx_path, temp_dir):
        """Test ~~strikethrough~~ formatting"""
        md = os.path.join(temp_dir, "strike.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Strikethrough\n\n")
            f.write("This is ~~strikethrough~~ text.\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        # Should complete even if strikethrough not fully supported
        assert result is True
        assert os.path.exists(output_docx_path)

    def test_nested_formatting(self, output_docx_path, temp_dir):
        """Test nested bold and italic"""
        md = os.path.join(temp_dir, "nested.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Nested Formatting\n\n")
            f.write("This is **bold with *italic inside***.\n")
            f.write("This is *italic with **bold inside***.\n")
            f.write("This is ***bold and italic***.\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True

    def test_escape_sequences(self, output_docx_path, temp_dir):
        """Test escaped markdown characters"""
        md = os.path.join(temp_dir, "escaped.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Escaped Characters\n\n")
            f.write(r"Escaped: \* \# \_ \[ \] \( \) \`")
            f.write("\n\n")
            f.write(r"Not bold: \*\*text\*\*" + "\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True

    def test_html_entities(self, output_docx_path, temp_dir):
        """Test HTML entities in markdown"""
        md = os.path.join(temp_dir, "entities.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# HTML Entities\n\n")
            f.write("&nbsp; &lt; &gt; &amp; &quot; &apos;\n")
            f.write("&copy; &reg; &trade;\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True


class TestLinksAndImages:
    """Test links and image references"""

    def test_inline_links(self, output_docx_path, temp_dir):
        """Test inline link format"""
        md = os.path.join(temp_dir, "links.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Links\n\n")
            f.write("[Google](https://google.com)\n")
            f.write("[Link with title](https://example.com \"Example\")\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True

    def test_reference_links(self, output_docx_path, temp_dir):
        """Test reference-style links"""
        md = os.path.join(temp_dir, "ref_links.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Reference Links\n\n")
            f.write("[Link text][ref]\n\n")
            f.write("[ref]: https://example.com\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True

    def test_images_with_alt_text(self, output_docx_path, temp_dir):
        """Test image references with alt text"""
        md = os.path.join(temp_dir, "images.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Images\n\n")
            f.write("![Alt text](image.png)\n")
            f.write("![Alt text](image.png \"Image title\")\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True


class TestListVariations:
    """Test various list formats"""

    def test_task_lists(self, output_docx_path, temp_dir):
        """Test GitHub-style task lists"""
        md = os.path.join(temp_dir, "tasks.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Task List\n\n")
            f.write("- [x] Completed task\n")
            f.write("- [ ] Incomplete task\n")
            f.write("- [x] Another completed task\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        # Should complete (checkboxes may not render perfectly)
        assert result is True

    def test_different_bullet_markers(self, output_docx_path, temp_dir):
        """Test -, *, + as bullet markers"""
        md = os.path.join(temp_dir, "bullets.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Different Bullets\n\n")
            f.write("- Hyphen bullet\n")
            f.write("* Asterisk bullet\n")
            f.write("+ Plus bullet\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True

    def test_lists_with_multiple_paragraphs(self, output_docx_path, temp_dir):
        """Test list items with multiple paragraphs"""
        md = os.path.join(temp_dir, "multi_para.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Multi-Paragraph Lists\n\n")
            f.write("- First item\n\n")
            f.write("  Second paragraph of first item\n\n")
            f.write("- Second item\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True


class TestCodeBlocks:
    """Test code block variations"""

    def test_fenced_code_with_language(self, output_docx_path, temp_dir):
        """Test code blocks with language specifier"""
        md = os.path.join(temp_dir, "code_lang.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Code with Language\n\n")
            f.write("```python\ndef hello():\n    print('Hello')\n```\n\n")
            f.write("```javascript\nconsole.log('Hello');\n```\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True

    def test_indented_code_blocks(self, output_docx_path, temp_dir):
        """Test 4-space indented code blocks"""
        md = os.path.join(temp_dir, "indented_code.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Indented Code\n\n")
            f.write("Normal text\n\n")
            f.write("    def hello():\n")
            f.write("        print('Hello')\n\n")
            f.write("More text\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True


class TestMiscFeatures:
    """Test miscellaneous markdown features"""

    def test_horizontal_rules(self, output_docx_path, temp_dir):
        """Test horizontal rules with various syntaxes"""
        md = os.path.join(temp_dir, "hr.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Horizontal Rules\n\n")
            f.write("---\n\n")
            f.write("***\n\n")
            f.write("___\n\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True

    def test_blockquotes_multiline(self, output_docx_path, temp_dir):
        """Test multi-line blockquotes"""
        md = os.path.join(temp_dir, "quotes.md")
        with open(md, 'w', encoding='utf-8') as f:
            f.write("# Blockquotes\n\n")
            f.write("> Line 1\n")
            f.write("> Line 2\n")
            f.write("> Line 3\n\n")
            f.write("> Nested\n")
            f.write(">> Quote\n")

        converter = MarkdownConverter()
        result = converter.markdown_to_word(md, output_docx_path)

        assert result is True
