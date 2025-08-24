import unittest
import pandas as pd
from unittest.mock import Mock, patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.data_processor import DataProcessor
from src.core.code_executor import CodeExecutor
from src.utils.code_parser import CodeParser
from src.utils.validators import Validators

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()
        self.sample_df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': ['a', 'b', 'c', 'd', 'e'],
            'C': [1.1, 2.2, None, 4.4, 5.5]
        })
    
    def test_analyze_dataframe(self):
        analysis = self.processor.analyze_dataframe(self.sample_df)
        
        self.assertEqual(analysis['shape'], (5, 3))
        self.assertEqual(len(analysis['columns']), 3)
        self.assertIn('A', analysis['numeric_columns'])
        self.assertIn('B', analysis['categorical_columns'])
        self.assertEqual(analysis['null_counts']['C'], 1)
    
    def test_clean_data(self):
        dirty_df = pd.DataFrame({
            'A': [1, 2, None, 4, 5],
            'B': ['a', 'b', None, 'd', 'e'],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        
        cleaned_df = self.processor.clean_data(dirty_df)
        
        # Check that missing values are filled
        self.assertEqual(cleaned_df['A'].isnull().sum(), 0)
        self.assertEqual(cleaned_df['B'].isnull().sum(), 0)

class TestCodeParser(unittest.TestCase):
    def setUp(self):
        self.parser = CodeParser()
    
    def test_match_code_blocks(self):
        text = """
        Here's some code:
        ```python
        print("Hello World")
        x = 5
        ```
        """
        
        code = self.parser.match_code_blocks(text)
        expected = 'print("Hello World")\nx = 5'
        self.assertEqual(code, expected)
    
    def test_validate_python_code(self):
        valid_code = "x = 5\nprint(x)"
        invalid_code = "x = 5\nprint(x"
        
        self.assertTrue(self.parser.validate_python_code(valid_code))
        self.assertFalse(self.parser.validate_python_code(invalid_code))

class TestValidators(unittest.TestCase):
    def setUp(self):
        self.validator = Validators()
        self.sample_df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': ['a', 'b', 'c', 'd', 'e']
        })
    
    def test_validate_dataframe(self):
        result = self.validator.validate_dataframe(self.sample_df)
        
        self.assertTrue(result['is_valid'])
        self.assertEqual(len(result['errors']), 0)
        self.assertEqual(result['info']['shape'], (5, 2))
    
    def test_validate_empty_dataframe(self):
        empty_df = pd.DataFrame()
        result = self.validator.validate_dataframe(empty_df)
        
        self.assertFalse(result['is_valid'])
        self.assertIn("DataFrame is empty", result['errors'])
    
    def test_validate_query(self):
        valid_query = "Show me the mean of column A"
        result = self.validator.validate_query(valid_query)
        
        self.assertTrue(result['is_valid'])
        self.assertEqual(len(result['errors']), 0)
    
    def test_validate_empty_query(self):
        empty_query = ""
        result = self.validator.validate_query(empty_query)
        
        self.assertFalse(result['is_valid'])
        self.assertIn("Query cannot be empty", result['errors'])

if __name__ == '__main__':
    unittest.main()