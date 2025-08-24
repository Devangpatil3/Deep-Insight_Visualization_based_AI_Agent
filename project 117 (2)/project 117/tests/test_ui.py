import unittest
from unittest.mock import Mock, patch
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.components import display_data_summary
from src.ui.output_handler import OutputHandler

class TestUIComponents(unittest.TestCase):
    def setUp(self):
        self.sample_df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': ['a', 'b', 'c', 'd', 'e'],
            'C': [1.1, 2.2, None, 4.4, 5.5]
        })
    
    @patch('streamlit.subheader')
    @patch('streamlit.columns')
    @patch('streamlit.metric')
    def test_display_data_summary(self, mock_metric, mock_columns, mock_subheader):
        # Mock streamlit columns
        mock_col = Mock()
        mock_columns.return_value = [mock_col, mock_col, mock_col, mock_col]
        mock_col.metric = Mock()
        
        # This would normally display in Streamlit, but we're just testing it doesn't crash
        try:
            display_data_summary(self.sample_df)
            test_passed = True
        except Exception:
            test_passed = False
        
        self.assertTrue(test_passed)

class TestOutputHandler(unittest.TestCase):
    def setUp(self):
        self.handler = OutputHandler()
    
    def test_process_results_with_string(self):
        results = ["Test output", "Another result"]
        
        # Mock streamlit functions
        with patch('streamlit.text') as mock_text:
            self.handler._process_results(results)
            # Should call st.text for each string result
            self.assertEqual(mock_text.call_count, 2)
    
    def test_display_dataframe_analysis(self):
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [2, 4, 6, 8, 10]
        })
        
        # Mock streamlit functions
        with patch('streamlit.subheader'), \
             patch('streamlit.tabs') as mock_tabs, \
             patch('streamlit.columns'):
            
            # Mock tabs context manager
            mock_tab = Mock()
            mock_tabs.return_value = [mock_tab, mock_tab, mock_tab, mock_tab]
            mock_tab.__enter__ = Mock(return_value=mock_tab)
            mock_tab.__exit__ = Mock(return_value=None)
            
            try:
                self.handler.display_dataframe_analysis(df)
                test_passed = True
            except Exception as e:
                test_passed = False
                print(f"Test failed with error: {e}")
            
            self.assertTrue(test_passed)

if __name__ == '__main__':
    unittest.main()