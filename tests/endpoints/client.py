import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    """
    Creates a test client for the FastAPI application.

    :return: TestClient instance
    :rtype: TestClient
    """
    return TestClient(app)
