"""Test configuration."""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client."""
    from jarvis_api.src.main import app
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Create authentication headers."""
    return {"Authorization": "Bearer test-token"}
