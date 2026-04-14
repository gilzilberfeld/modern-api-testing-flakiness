"""
SUSPECT 5: Environment & Configuration

THE ASSUMPTION: "The environment matches what I expect."

These tests demonstrate flakiness caused by:
1. Hardcoded file paths that only work on specific OS
2. Assuming Linux filesystem structure on Windows (or vice versa)
3. Config files in OS-specific locations

To simulate the flakiness:
- Run on Windows: Tests fail because /etc/app/config.json doesn't exist
- Run on Linux: Tests might pass if you create the config file
"""

import json
import requests

# FLAKY: Hardcoded Linux-style absolute path
CONFIG_PATH = "/etc/bookstore/server_config.json"


def get_server_url():
    """
    Reads server URL from config file.

    FLAKY BECAUSE: Uses hardcoded Linux path that doesn't exist on Windows.
    On Linux, /etc/ is a standard config location.
    On Windows, this path is completely invalid.
    """
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    return config["server_url"]


# =============================================================================
# TEST 1: Get books using config-based server URL
# =============================================================================

def test_get_books_from_configured_server():
    """
    Gets the list of books from the server URL specified in config.

    FLAKY BECAUSE: The config file path is hardcoded for Linux.
    - On Linux: Might work if /etc/bookstore/server_config.json exists
    - On Windows: Always fails with FileNotFoundError
    - On CI: Fails unless the CI setup creates this specific file
    """
    server_url = get_server_url()

    response = requests.get(f"{server_url}/books")
    assert response.status_code == 200

    books = response.json()
    assert len(books) >= 1, "Should have at least one book"


# =============================================================================
# TEST 2: Get server health using config-based URL
# =============================================================================

def test_server_health_from_configured_url():
    """
    Checks server health using the configured server URL.

    FLAKY BECAUSE: Same issue - Linux-specific path assumption.
    The test logic is fine, but it can never run on Windows
    because it can't even read the configuration.
    """
    server_url = get_server_url()

    response = requests.get(f"{server_url}/health")
    assert response.status_code == 200

    health = response.json()
    assert health["status"] == "healthy"
