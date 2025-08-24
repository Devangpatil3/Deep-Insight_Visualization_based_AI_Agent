import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging

class DataProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze dataframe and return comprehensive information"""
        try:
            analysis = {
                'shape': df.shape,
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict(),
                'memory_usage': df.memory_usage(deep=True).sum(),
                'null_counts': df.isnull().sum().to_dict(),
                'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
                'categorical_columns': df.select_dtypes(include=['object']).columns.tolist(),
                'datetime_columns': df.select_dtypes(include=['datetime64']).columns.tolist(),
            }
            
            # Statistical summary for numeric columns
            if analysis['numeric_columns']:
                analysis['numeric_summary'] = df[analysis['numeric_columns']].describe().to_dict()
            
            # Value counts for categorical columns (top 5)
            if analysis['categorical_columns']:
                analysis['categorical_summary'] = {}
                for col in analysis['categorical_columns']:
                    analysis['categorical_summary'][col] = df[col].value_counts().head().to_dict()
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Data analysis error: {str(e)}")
            return {}
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Basic data cleaning operations"""
        try:
            # Remove duplicate rows
            df_cleaned = df.drop_duplicates()
            
            # Handle missing values (basic strategy)
            numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
            df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(df_cleaned[numeric_cols].median())
            
            categorical_cols = df_cleaned.select_dtypes(include=['object']).columns
            df_cleaned[categorical_cols] = df_cleaned[categorical_cols].fillna(df_cleaned[categorical_cols].mode().iloc[0] if not df_cleaned[categorical_cols].mode().empty else 'Unknown')
            
            return df_cleaned
            
        except Exception as e:
            self.logger.error(f"Data cleaning error: {str(e)}")
            return df