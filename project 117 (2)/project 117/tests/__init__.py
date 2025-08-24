"""
Test package initialization.
This file makes the tests directory a Python package.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

# Test configuration
TEST_DATA_DIR = "tests/test_data"
SAMPLE_CSV_FILE = f"{TEST_DATA_DIR}/sample_data.csv"
SAMPLE_XLSX_FILE = f"{TEST_DATA_DIR}/sample_data.xlsx"
SAMPLE_JSON_FILE = f"{TEST_DATA_DIR}/sample_data.json"

# Common test utilities
def get_test_data_path(filename):
    """Get the full path to a test data file."""
    return f"{TEST_DATA_DIR}/{filename}"

# Test constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3