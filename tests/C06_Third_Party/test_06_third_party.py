"""
SUSPECT 6: Third-Party Dependencies

THE ASSUMPTION: "External services behave consistently."

These tests demonstrate flakiness caused by:
1. Depending on external files that may or may not exist
2. Depending on third-party services that are unreliable

To simulate the flakiness:
- Delete the config file to break test 1
- Run test 2 multiple times - it will fail ~30% of the time
"""

import json
import requests

BASE_URL = "http://localhost:5000"

# FLAKY: Hardcoded path to config file that may not exist
CONFIG_FILE = "/etc/bookstore/settings.json"


# =============================================================================
# TEST 1: Depends on external config file
# =============================================================================

def test_load_settings_and_verify_server():
    """
    Loads settings from a config file and verifies the server is running.

    FLAKY BECAUSE: The config file may not exist on all machines.
    - Works on developer's machine where they created the file
    - Fails on CI server where no one set it up
    - Fails on colleague's machine who never created it
    """
    # Try to load settings from external file
    with open(CONFIG_FILE, "r") as f:
        settings = json.load(f)

    server_url = settings.get("server_url", BASE_URL)

    # Verify server is available
    response = requests.get(f"{server_url}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# =============================================================================
# TEST 2: Depends on unreliable payment service
# =============================================================================

def test_create_order_with_payment():
    """
    Creates an order - the server internally calls the payment gateway.

    FLAKY BECAUSE: The POST /orders endpoint internally calls process_payment()
    which has a 30% failure rate.
    - Sometimes passes, sometimes fails with 503
    - No way to predict when it will fail
    - The test code looks perfectly fine, but fails randomly
    """
    # Create an order - server calls payment gateway internally
    order_response = requests.post(f"{BASE_URL}/orders", json={
        "book_id": "book-1",
        "user_id": 1
    })

    # FLAKY: This assertion fails ~30% of the time due to payment gateway!
    assert order_response.status_code == 201, \
        f"Order failed: {order_response.json()}"

    order = order_response.json()
    assert order["status"] == "confirmed"
    assert "transaction_id" in order
