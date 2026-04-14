"""
Bigger Better Bookstore - Test Configuration

Shared fixtures for the flaky API tests demo.
"""

import pytest
import subprocess
import time
import requests
import sys
import os

# Add the project root to path so we can import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_client import BookstoreClient


BASE_URL = "http://localhost:5000"


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the API server."""
    return BASE_URL


@pytest.fixture
def client():
    """Returns a BookstoreClient instance."""
    return BookstoreClient(BASE_URL)


@pytest.fixture
def clean_state(client):
    """
    Resets the server to a clean state before AND after the test.
    Use this fixture when you want a truly isolated test.
    """
    client.reset()
    yield
    client.reset()


def wait_for_server(url: str, timeout: int = 10) -> bool:
    """Wait for the server to be ready."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(f"{url}/health")
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            pass
        time.sleep(0.1)
    return False


# Note: We don't auto-start the server as a fixture because:
# 1. For the webinar, Gil will run the server manually so audience can see it
# 2. It makes the flakiness more visible when the server state persists
# 3. Some tests specifically need to demonstrate state pollution across runs
#
# To run tests, start the server first:
#   python src/server.py
#
# Then run tests:
#   pytest tests/
