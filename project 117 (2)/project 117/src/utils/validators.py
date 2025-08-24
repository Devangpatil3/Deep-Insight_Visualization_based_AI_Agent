import pandas as pd
import re
from typing import List, Dict, Any, Optional
import logging

class Validators:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate DataFrame and return validation results"""
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'info': {}
        }
        
        try:
            # Check if DataFrame is empty
            if df.empty:
                validation_results['errors'].append("DataFrame is empty")
                validation_results['is_valid'] = False
                return validation_results
            
            # Check for minimum columns
            if len(df.columns) < 1:
                validation_results['errors'].append("DataFrame has no columns")
                validation_results['is_valid'] = False
            
            # Check for duplicate columns
            if len(df.columns) != len(set(df.columns)):
                validation_results['warnings'].append("DataFrame has duplicate column names")
            
            # Check for excessive missing values
            null_percentages = (df.isnull().sum() / len(df)) * 100
            high_null_cols = null_percentages[null_percentages > 50].index.tolist()
            if high_null_cols:
                validation_results['warnings'].append(f"Columns with >50% missing values: {high_null_cols}")
            
            # Add info
            validation_results['info'] = {
                'shape': df.shape,
                'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB",
                'dtypes': df.dtypes.value_counts().to_dict()
            }
            
        except Exception as e:
            validation_results['errors'].append(f"Validation error: {str(e)}")
            validation_results['is_valid'] = False
            self.logger.error(f"DataFrame validation error: {str(e)}")
        
        return validation_results
    
    def validate_query(self, query: str) -> Dict[str, Any]:
        """Validate user query"""
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            # Check if query is empty
            if not query or not query.strip():
                validation_results['errors'].append("Query cannot be empty")
                validation_results['is_valid'] = False
                return validation_results
            
            # Check query length
            if len(query) < 5:
                validation_results['warnings'].append("Query seems too short")
            elif len(query) > 1000:
                validation_results['warnings'].append("Query is very long")
            
            # Check for potentially harmful content
            dangerous_patterns = [
                r'import\s+os',
                r'import\s+subprocess',
                r'eval\s*\(',
                r'exec\s*\(',
                r'__import__',
                r'open\s*\(',
                r'file\s*\(',
                r'input\s*\('
            ]
            
            for pattern in dangerous_patterns:
                if re.search(pattern, query, re.IGNORECASE):
                    validation_results['warnings'].append("Query contains potentially unsafe operations")
                    break
            
        except Exception as e:
            validation_results['errors'].append(f"Query validation error: {str(e)}")
            validation_results['is_valid'] = False
            self.logger.error(f"Query validation error: {str(e)}")
        
        return validation_results