import io
import contextlib
import warnings
from typing import Optional, List, Any, Tuple
import streamlit as st
from e2b_code_interpreter import Sandbox
import logging

class CodeExecutor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def execute_code(self, e2b_code_interpreter: Sandbox, code: str) -> Tuple[Optional[List[Any]], str]:
        """Execute Python code in E2B sandbox"""
        
        with st.spinner('🔧 Executing code in E2B sandbox...'):
            try:
                stdout_capture = io.StringIO()
                stderr_capture = io.StringIO()

                with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        exec_result = e2b_code_interpreter.run_code(code)

                stderr_output = stderr_capture.getvalue()
                stdout_output = stdout_capture.getvalue()

                if stderr_output:
                    st.error(f"⚠️ Error during execution:\n{stderr_output}")
                    self.logger.error(f"Code execution error: {stderr_output}")

                results = []
                if exec_result.results:
                    results.extend(exec_result.results)
                if stdout_output.strip():
                    results.append(stdout_output.strip())

                return results if results else None, stdout_output.strip()
                
            except Exception as e:
                self.logger.error(f"Code execution error: {str(e)}")
                st.error(f"❌ Code execution failed: {str(e)}")
                return None, ""