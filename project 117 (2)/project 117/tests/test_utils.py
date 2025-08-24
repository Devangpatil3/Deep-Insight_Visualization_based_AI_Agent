import unittest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.file_handler import FileHandler
from src.utils.code_parser import CodeParser
from src.utils.validators import Validators

class TestFileHandler(unittest.TestCase):
    def setUp(self):
        self.handler = FileHandler()
    
    def test_validate_file_size(self):
        # Mock file object
        mock_file = Mock()
        mock_file.getvalue.return_value = b'x' * (50 * 1024 * 1024)  # 50MB
        
        # Test with 100MB limit (should pass)
        self.assertTrue(self.handler.validate_file_size(mock_file, 100))
        
        # Test with 10MB limit (should fail)
        self.assertFalse(self.handler.validate_file_size(mock_file, 10))
    
    @patch('pandas.read_csv')
    def test_process_csv_file(self, mock_read_csv):
        mock_file = Mock()
        mock_file.name = 'test.csv'
        mock_df = pd.DataFrame({'A': [1, 2, 3]})
        mock_read_csv.return_value = mock_df
        
        result = self.handler.process_file(mock_file)
        
        self.assertIsInstance(result, pd.DataFrame)
        mock_read_csv.assert_called_once_with(mock_file)

class TestCodeParserAdvanced(unittest.TestCase):
    def setUp(self):
        self.parser = CodeParser()
    
    def test_extract_multiple_code_blocks(self):
        text = """
        First block:
        ```python
        x = 1
        ```
        
        Second block:
        ```python
        y = 2
        ```
        """
        
        code_blocks = self.parser.extract_all_code_blocks(text)
        self.assertEqual(len(code_blocks), 2)
        self.assertEqual(code_blocks[0].strip(), 'x = 1')
        self.assertEqual(code_blocks[1].strip(), 'y = 2')
    
    def test_no_code_blocks(self):
        text = "This is just regular text with no code blocks."
        code_blocks = self.parser.extract_all_code_blocks(text)
        self.assertEqual(len(code_blocks), 0)

class TestValidatorsAdvanced(unittest.TestCase):
    def setUp(self):
        self.validator = Validators()
    
    def test_validate_dataframe_with_high_null_values(self):
        # Create DataFrame with high null percentage
        df = pd.DataFrame({
            'A': [1, None, None, None, None],
            'B': [1, 2, 3, 4, 5]
        })
        
        result = self.validator.validate_dataframe(df)
        
        # Should still be valid but have warnings
        self.assertTrue(result['is_valid'])
        self.assertTrue(any('missing values' in warning.lower() for warning in result['warnings']))
    
    def test_validate_suspicious_query(self):
        suspicious_query = "import os; os.system('rm -rf /')"
        result = self.validator.validate_query(suspicious_query)
        
        # Should be valid but have warnings about unsafe operations
        self.assertTrue(result['is_valid'])
        self.assertTrue(any('unsafe' in warning.lower() for warning in result['warnings']))

if __name__ == '__main__':
    unittest.main()