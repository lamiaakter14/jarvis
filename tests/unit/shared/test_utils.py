"""Tests for utility functions."""

import pytest
from jarvis_core.shared.utils import sanitize_filename


@pytest.mark.unit
class TestSanitizeFilename:
    """Test cases for sanitize_filename function."""
    
    def test_basic_filename(self):
        """Test sanitization of basic valid filename."""
        assert sanitize_filename("test.txt") == "test.txt"
        assert sanitize_filename("document.pdf") == "document.pdf"
    
    def test_remove_invalid_characters(self):
        """Test removal of invalid filesystem characters."""
        assert sanitize_filename('file<name>.txt') == 'filename.txt'
        assert sanitize_filename('file>name>.txt') == 'filename.txt'
        assert sanitize_filename('file:name.txt') == 'filename.txt'
        assert sanitize_filename('file"name.txt') == 'filename.txt'
        # Note: slashes are treated as path separators, so only last component is kept
        assert sanitize_filename('file/name.txt') == 'name.txt'
        assert sanitize_filename('file\\name.txt') == 'name.txt'
        assert sanitize_filename('file|name.txt') == 'filename.txt'
        assert sanitize_filename('file?name.txt') == 'filename.txt'
        assert sanitize_filename('file*name.txt') == 'filename.txt'
    
    def test_path_traversal_protection(self):
        """Test protection against path traversal attacks."""
        assert sanitize_filename('../../../etc/passwd') == 'passwd'
        assert sanitize_filename('..\\..\\windows\\system32') == 'system32'
        assert sanitize_filename('/etc/passwd') == 'passwd'
        assert sanitize_filename('C:\\Windows\\System32\\config') == 'config'
    
    def test_space_replacement(self):
        """Test space replacement with underscores."""
        assert sanitize_filename('my file name.txt') == 'my_file_name.txt'
        assert sanitize_filename('multiple   spaces.txt') == 'multiple_spaces.txt'
    
    def test_strip_dots_and_spaces(self):
        """Test removal of leading/trailing dots and spaces."""
        assert sanitize_filename('  file.txt  ') == 'file.txt'
        assert sanitize_filename('..file.txt') == 'file.txt'
        assert sanitize_filename('file.txt..') == 'file.txt'
        # This unusual input leaves internal underscores from dot-space combinations
        assert sanitize_filename('. . file . .txt') == 'file_._.txt'
    
    def test_windows_reserved_names(self):
        """Test handling of Windows reserved filenames."""
        assert sanitize_filename('CON') == '_CON'
        assert sanitize_filename('con') == '_con'
        assert sanitize_filename('PRN.txt') == '_PRN.txt'
        assert sanitize_filename('AUX.log') == '_AUX.log'
        assert sanitize_filename('NUL') == '_NUL'
        assert sanitize_filename('COM1') == '_COM1'
        assert sanitize_filename('LPT1.dat') == '_LPT1.dat'
    
    def test_control_characters(self):
        """Test removal of control characters."""
        result = sanitize_filename('file\x00name.txt')
        assert '\x00' not in result
        assert result == 'filename.txt'
        
        result = sanitize_filename('file\x1fname.txt')
        assert '\x1f' not in result
        assert result == 'filename.txt'
    
    def test_max_length_truncation(self):
        """Test filename length truncation."""
        long_name = 'a' * 300 + '.txt'
        result = sanitize_filename(long_name, max_length=255)
        assert len(result) <= 255
        assert result.endswith('.txt')
        
        long_name_no_ext = 'a' * 300
        result = sanitize_filename(long_name_no_ext, max_length=255)
        assert len(result) <= 255
    
    def test_preserve_extension(self):
        """Test that extension is preserved during truncation."""
        long_name = 'a' * 300 + '.extension'
        result = sanitize_filename(long_name, max_length=50)
        assert len(result) <= 50
        assert result.endswith('.extension')
    
    def test_empty_filename_raises(self):
        """Test that empty filename raises ValueError."""
        with pytest.raises(ValueError, match="Filename cannot be empty"):
            sanitize_filename('')
        
        with pytest.raises(ValueError, match="Filename cannot be empty"):
            sanitize_filename('   ')
    
    def test_filename_becomes_empty_after_sanitization(self):
        """Test that filename becoming empty after sanitization raises ValueError."""
        with pytest.raises(ValueError, match="Filename becomes empty after sanitization"):
            sanitize_filename('...')
        
        with pytest.raises(ValueError, match="Filename becomes empty after sanitization"):
            sanitize_filename('   ...   ')
    
    def test_multiple_dots_in_filename(self):
        """Test handling of multiple dots in filename."""
        assert sanitize_filename('file.name.with.dots.txt') == 'file.name.with.dots.txt'
        assert sanitize_filename('archive.tar.gz') == 'archive.tar.gz'
    
    def test_unicode_characters(self):
        """Test handling of unicode characters (should be preserved)."""
        assert sanitize_filename('файл.txt') == 'файл.txt'
        assert sanitize_filename('文件.txt') == '文件.txt'
        assert sanitize_filename('αρχείο.txt') == 'αρχείο.txt'
    
    def test_underscore_consolidation(self):
        """Test that multiple underscores are consolidated."""
        assert sanitize_filename('file___name.txt') == 'file_name.txt'
        assert sanitize_filename('file  _  name.txt') == 'file_name.txt'
    
    def test_complex_real_world_examples(self):
        """Test complex real-world filename scenarios."""
        # Parentheses and brackets are removed for maximum compatibility
        assert sanitize_filename('My Document (Draft) v2.1 [FINAL].docx') == 'My_Document_Draft_v2.1_FINAL.docx'
        assert sanitize_filename('report_2024-01-15.pdf') == 'report_2024-01-15.pdf'
        assert sanitize_filename('image  copy (2).jpg') == 'image_copy_2.jpg'
