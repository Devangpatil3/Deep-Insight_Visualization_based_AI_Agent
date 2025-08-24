import pandas as pd
import json
import logging
from typing import Optional
import streamlit as st
from e2b_code_interpreter import Sandbox

class FileHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_formats = ['csv', 'xlsx', 'json']
    
    def process_file(self, uploaded_file) -> Optional[pd.DataFrame]:
        """Process uploaded file and return DataFrame"""
        try:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'csv':
                return pd.read_csv(uploaded_file)
            elif file_extension in ['xlsx', 'xls']:
                return pd.read_excel(uploaded_file)
            elif file_extension == 'json':
                data = json.load(uploaded_file)
                if isinstance(data, list):
                    return pd.DataFrame(data)
                elif isinstance(data, dict):
                    return pd.DataFrame([data])
                else:
                    raise ValueError("Invalid JSON structure")
            else:
                st.error(f"Unsupported file format: {file_extension}")
                return None
                
        except Exception as e:
            self.logger.error(f"File processing error: {str(e)}")
            st.error(f"Error processing file: {str(e)}")
            return None
    
    def upload_to_sandbox(self, code_interpreter: Sandbox, uploaded_file) -> str:
        """Upload file to E2B sandbox"""
        dataset_path = f"./{uploaded_file.name}"
        try:
            code_interpreter.files.write(dataset_path, uploaded_file)
            return dataset_path
        except Exception as error:
            st.error(f"Error during file upload: {error}")
            self.logger.error(f"Sandbox upload error: {error}")
            raise error
    
    def validate_file_size(self, file, max_size_mb=100):
        """Validate file size"""
        file_size = len(file.getvalue()) / (1024 * 1024)  # Convert to MB
        return file_size <= max_size_mb