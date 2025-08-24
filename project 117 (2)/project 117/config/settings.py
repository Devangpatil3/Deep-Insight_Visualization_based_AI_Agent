import os
from dotenv import load_dotenv

load_dotenv()

# App Configuration
APP_CONFIG = {
    'title': 'AI Data Visualization Agent',
    'version': '1.0.0',
    'debug': os.getenv('DEBUG', 'False').lower() == 'true',
    'max_file_size': os.getenv('MAX_FILE_SIZE', '100MB'),
    'supported_formats': ['csv', 'xlsx', 'json'],
    'cache_ttl': int(os.getenv('CACHE_TTL', '3600'))
}

# API Configuration
API_CONFIG = {
    'together_api_key': os.getenv('TOGETHER_API_KEY'),
    'e2b_api_key': os.getenv('E2B_API_KEY'),
    'default_model': os.getenv('DEFAULT_MODEL', 'meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo'),
    'max_tokens': 4000,
    'temperature': 0.7
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'handlers': ['file', 'console']
}