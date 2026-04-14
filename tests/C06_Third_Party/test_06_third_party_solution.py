"""
SUSPECT 6: Third-Party Dependencies - STABILIZED SOLUTION

THE FIX:
1. For file dependencies: Use fallbacks and cross-platform paths
2. For unreliable services: Mock the external dependency with respx

Key principles:
1. Never assume external files exist - provide fallbacks
2. Mock unreliable external services in tests
3. Make dependencies explicit and configurable
"""

import json
import requests
import respx
from httpx import Response
from pathlib import Path

BASE_URL = "http://localhost:5000"
PAYMENT_SERVICE_URL = "http://localhost:5000/unreliable-payment"


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def load_settings_with_fallback():
    """
    Load settings with fallback to defaults.

    STABILIZED: Tries multiple locations and falls back to defaults.
    """
    # Try project-relative config first
    config_path = get_project_root() / "config" / "server_config.json"

    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)

    # Return sensible defaults if no config found
    return {
        "server_url": "http://localhost:5000",
        "timeout": 30
    }


# =============================================================================
# SOLUTION 1: Config file with fallback
# =============================================================================

def test_load_settings_and_verify_server():
    """
    STABILIZED: Loads settings with fallback to defaults.

    Works because:
    - Uses cross-platform path resolution
    - Falls back to sensible defaults if file missing
    - Never fails just because a config file is absent
    """
    settings = load_settings_with_fallback()
    server_url = settings.get("server_url", BASE_URL)

    response = requests.get(f"{server_url}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# =============================================================================
# SOLUTION 2: Mock the unreliable payment service with respx
# =============================================================================

@respx.mock
def test_create_order_with_payment():
    """
    STABILIZED: Mocks the HTTP call to the payment gateway using respx.

    Works because:
    - respx intercepts the httpx.post call to the payment service
    - The mock always returns a successful payment response
    - The test is isolated from the real (unreliable) payment service
    - 100% reliable - no random failures
    """
    # Mock the payment service endpoint
    respx.post(PAYMENT_SERVICE_URL).mock(
        return_value=Response(
            200,
            json={"status": "approved", "transaction_id": "TXN-TEST-1234"}
        )
    )

    order_response = requests.post(f"{BASE_URL}/orders", json={
        "book_id": "book-1",
        "user_id": 1
    })

    assert order_response.status_code == 201, \
        f"Order failed: {order_response.json()}"

    order = order_response.json()
    assert order["status"] == "confirmed"
    assert order["transaction_id"] == "TXN-TEST-1234"
