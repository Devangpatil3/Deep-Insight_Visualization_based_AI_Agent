import re
import warnings
from typing import Optional, List, Any, Tuple
import streamlit as st
from together import Together
from e2b_code_interpreter import Sandbox
from src.core.code_executor import CodeExecutor
from src.utils.code_parser import CodeParser
from config.settings import API_CONFIG
import logging

class LLMClient:
    def __init__(self):
        self.code_executor = CodeExecutor()
        self.code_parser = CodeParser()
        self.logger = logging.getLogger(__name__)
    
    def chat_with_llm(self, e2b_code_interpreter: Sandbox, user_message: str, dataset_path: str) -> Tuple[Optional[List[Any]], str, str]:
        """Chat with LLM and execute generated code"""
        
        system_prompt = f"""You're a Python data scientist and data visualization expert. You are given a dataset at path '{dataset_path}' and also the user's query.
You need to analyze the dataset and answer the user's query with a response and you run Python code to solve them.
IMPORTANT: Always use the dataset path variable '{dataset_path}' in your code when reading the CSV file.
Also return the result/output of the code execution along with the code itself.

Guidelines:
- Use pandas for data analysis
- Use matplotlib, seaborn, or plotly for visualizations
- Provide clear, executable Python code
- Include proper error handling
- Show results and insights from the analysis
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        with st.spinner('🤖 Getting response from Together AI LLM model...'):
            try:
                client = Together(api_key=st.session_state.together_api_key)
                response = client.chat.completions.create(
                    model=st.session_state.model_name,
                    messages=messages,
                    max_tokens=API_CONFIG['max_tokens'],
                    temperature=API_CONFIG['temperature']
                )

                response_message = response.choices[0].message
                python_code = self.code_parser.match_code_blocks(response_message.content)

                if python_code:
                    code_results, stdout_output = self.code_executor.execute_code(
                        e2b_code_interpreter, python_code
                    )
                    return code_results, response_message.content, python_code
                else:
                    st.warning(f"⚠️ No Python code block detected in LLM's response.")
                    return None, response_message.content, ""
                    
            except Exception as e:
                self.logger.error(f"LLM API error: {str(e)}")
                st.error(f"❌ Error communicating with LLM: {str(e)}")
                return None, "", ""