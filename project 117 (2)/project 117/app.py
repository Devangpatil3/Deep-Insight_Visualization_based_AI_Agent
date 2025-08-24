import os
import json
import re
import sys
import io
import contextlib
import warnings
from typing import Optional, List, Any, Tuple
from PIL import Image
import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from together import Together
from e2b_code_interpreter import Sandbox

from src.core.llm_client import LLMClient
from src.core.code_executor import CodeExecutor
from src.core.data_processor import DataProcessor
from src.utils.file_handler import FileHandler
from src.utils.code_parser import CodeParser
from src.ui.sidebar import setup_sidebar
from src.ui.components import display_header, display_footer, display_data_summary
from src.ui.output_handler import OutputHandler
from config.settings import APP_CONFIG, API_CONFIG
import logging

# Configure logging
logging.basicConfig(
    filename='logs/app.log', 
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

def main():
    """Main application function"""
    st.set_page_config(
        page_title="AI Data Visualization Agent",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    display_header()
    
    # Initialize components
    llm_client = LLMClient()
    code_executor = CodeExecutor()
    data_processor = DataProcessor()
    file_handler = FileHandler()
    code_parser = CodeParser()
    output_handler = OutputHandler()
    
    # Setup sidebar
    setup_sidebar()
    
    # Main content
    uploaded_file = st.file_uploader("📂 Upload CSV file", type="csv")
    
    if uploaded_file is not None:
        # Process and display data
        df = pd.read_csv(uploaded_file)
        st.write("🧾 **Dataset Preview:**")
        
        if st.checkbox("🔎 Show full dataset"):
            st.dataframe(df)
        else:
            st.dataframe(df.head())
        
        # Display data summary
        display_data_summary(df)
        
        # Query input
        query = st.text_area(
            "💬 Ask a question about your data:",
            "Can you calculate and display the mean of each numerical column?"
        )
        
        if st.button("🔍 Analyze", type="primary"):
            if not st.session_state.together_api_key or not st.session_state.e2b_api_key:
                st.error("Please enter both API keys in the sidebar.")
            else:
                try:
                    with Sandbox(api_key=st.session_state.e2b_api_key) as code_interpreter:
                        # Upload dataset to sandbox
                        dataset_path = file_handler.upload_to_sandbox(code_interpreter, uploaded_file)
                        
                        # Get LLM response and execute code
                        code_results, llm_response, exec_code = llm_client.chat_with_llm(
                            code_interpreter, query, dataset_path
                        )
                        
                        # Display results
                        output_handler.display_results(code_results, llm_response, exec_code)
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    logging.error(f"Analysis error: {str(e)}")
    
    display_footer()

if __name__ == "__main__":
    main()