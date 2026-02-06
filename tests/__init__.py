"""
Test Suite for StudyBuddy

Contains all unit tests, integration tests, and fixtures.
"""

# Add common test fixtures or utilities here if needed
import sys
from pathlib import Path

# Ensure the backend directory is in the Python path
backend_dir = Path(__file__).parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))