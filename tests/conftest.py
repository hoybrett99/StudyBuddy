# tests/conftest.py

import pytest
import os
import sys
from pathlib import Path

# Ensure backend is importable
backend_dir = Path(__file__).parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Setup test environment before running any tests.
    This runs automatically for all tests.
    """
    # Set required environment variables for testing
    os.environ["GOOGLE_API_KEY"] = "test_google_key_for_testing"
    os.environ["CLAUDE_API_KEY"] = "test_claude_key_for_testing"
    
    yield  # Tests run here
    
    # Cleanup after all tests (if needed)
    pass