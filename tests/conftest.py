"""Pytest configuration and shared fixtures."""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import all fixtures to make them available to tests
pytest_plugins = [
    "tests.fixtures.domain_fixtures",
    "tests.fixtures.repository_fixtures",
]
