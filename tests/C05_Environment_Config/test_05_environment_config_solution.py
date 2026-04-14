"""
SUSPECT 5: Environment & Configuration - STABILIZED SOLUTION

THE FIX: Use platform-independent paths and configuration methods.

Key principles:
1. Use relative paths from the project root, not absolute OS-specific paths
2. Use pathlib for cross-platform path handling
3. Use environment variables as overrides
4. Provide sensible defaults when config is missing
"""

import json
import os
import requests
from pathlib import Path


def get_project_root():
    """Get the project root directory (works on any OS)."""
    # Navigate up from tests/C05_Environment_Config to project root
    return Path(__file__).parent.parent.parent


def get_config_path():
    """
    Get config file path in a cross-platform way.

    Priority:
    1. CONFIG_PATH environment variable (for CI/custom setups)
    2. Relative path from project root (works on any OS)
    """
    # Allow override via environment variable
    if os.environ.get("CONFIG_PATH"):
        return Path(os.environ["CONFIG_PATH"])

    # Use relative path from project root - works on Windows, Linux, Mac
    return get_project_root() / "config" / "server_config.json"


def get_server_url():
    """
    Reads server URL from config file with fallback.

    STABILIZED:
    - Uses cross-platform path resolution
    - Allows environment variable override for server URL
    - Provides default if config is missing
    """
    # First priority: environment variable
    if os.environ.get("SERVER_URL"):
        return os.environ["SERVER_URL"]

    # Second priority: config file
    config_path = get_config_path()

    if config_path.exists():
        with open(config_path, "r") as f:
            config = json.load(f)
        return config.get("server_url", "http://localhost:5000")

    # Fallback default
    return "http://localhost:5000"


# =============================================================================
# TEST 1: Get books using config-based server URL
# =============================================================================

def test_get_books_from_configured_server():
    """
    STABILIZED: Gets books using cross-platform configuration.

    Works on any OS because:
    - Path is relative to project root using pathlib
    - Falls back to default if config missing
    - Can be overridden via SERVER_URL env var
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
    STABILIZED: Checks server health using cross-platform config.

    Works on any OS and any CI environment.
    """
    server_url = get_server_url()

    response = requests.get(f"{server_url}/health")
    assert response.status_code == 200

    health = response.json()
    assert health["status"] == "healthy"
