import re
from typing import List, Optional
import logging

class CodeParser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.pattern = re.compile(r"```python\n(.*?)\n```", re.DOTALL)
    
    def match_code_blocks(self, llm_response: str) -> str:
        """Extract Python code blocks from LLM response"""
        try:
            match = self.pattern.search(llm_response)
            if match:
                return match.group(1)
            
            # Fallback: try to find code without markdown
            lines = llm_response.split('\n')
            code_lines = []
            in_code_block = False
            
            for line in lines:
                if line.strip().startswith('```python'):
                    in_code_block = True
                    continue
                elif line.strip().startswith('```') and in_code_block:
                    break
                elif in_code_block:
                    code_lines.append(line)
            
            return '\n'.join(code_lines) if code_lines else ""
            
        except Exception as e:
            self.logger.error(f"Code parsing error: {str(e)}")
            return ""
    
    def extract_all_code_blocks(self, text: str) -> List[str]:
        """Extract all code blocks from text"""
        try:
            matches = self.pattern.findall(text)
            return matches if matches else []
        except Exception as e:
            self.logger.error(f"Multiple code extraction error: {str(e)}")
            return []
    
    def validate_python_code(self, code: str) -> bool:
        """Basic validation of Python code syntax"""
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError as e:
            self.logger.warning(f"Code syntax error: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Code validation error: {str(e)}")
            return False