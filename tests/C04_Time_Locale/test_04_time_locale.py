"""
SUSPECT 4: Time & Locale

THE ASSUMPTION: "Time and location are fixed."

These tests demonstrate flakiness caused by:
1. Tests running near midnight UTC - order created "today" might be "yesterday" moments later
2. Timezone differences between test environment and server
3. Date format assumptions that vary by locale

To simulate the flakiness:
- Run with different TZ environment variable: TZ=UTC vs TZ=Pacific/Auckland
- Run tests near midnight UTC
- Change system locale settings
"""

import requests
from datetime import datetime

BASE_URL = "http://localhost:5000"


def setup_module():
    """Reset server state before tests."""
    requests.post(f"{BASE_URL}/reset")


# =============================================================================
# TEST 1: Create an order and expect it in "today's orders"
# =============================================================================

def test_create_order_appears_in_todays_orders():
    """
    Creates an order and verifies it shows up in today's orders.

    FLAKY BECAUSE: The server uses UTC for "today". If this test runs at
    11:00 PM in New York (UTC-5), it's already 4:00 AM "tomorrow" in UTC.
    The order gets created with tomorrow's UTC date, but the developer
    expects it to be in "today's" orders based on their local time.

    Also fails when test runs at 23:59:59 UTC and the assertion runs
    at 00:00:01 UTC the next day.
    """
    # Create an order
    order_response = requests.post(f"{BASE_URL}/orders", json={
        "book_id": "book-1",
        "user_id": 1
    })
    assert order_response.status_code == 201
    created_order = order_response.json()
    order_id = created_order["id"]

    # Get today's orders - expect our order to be there
    todays_response = requests.get(f"{BASE_URL}/orders/today")
    assert todays_response.status_code == 200
    todays_orders = todays_response.json()

    # FLAKY: This assumes "today" means the same thing to us and the server
    order_ids = [o["id"] for o in todays_orders]
    assert order_id in order_ids, f"Order {order_id} not found in today's orders!"


# =============================================================================
# TEST 2: Validate date format in order response
# =============================================================================

def test_order_date_format_matches_expected():
    """
    Creates an order and validates the date format.

    FLAKY BECAUSE: The test hardcodes an expected date format that may not
    match across locales or when the server's locale configuration changes.
    Different systems may format dates as:
    - 2024-01-15 (ISO)
    - 01/15/2024 (US)
    - 15/01/2024 (EU)
    - 15.01.2024 (German)

    The test also extracts "today's date" from the local system, which may
    differ from the server's UTC date.
    """
    # Create an order
    order_response = requests.post(f"{BASE_URL}/orders", json={
        "book_id": "book-2",
        "user_id": 1
    })
    assert order_response.status_code == 201
    order = order_response.json()

    # FLAKY: Assumes server date matches local machine's date
    expected_date = datetime.now().strftime("%Y-%m-%d")

    # FLAKY: Assumes ISO format and that dates match
    assert order["created_at"].startswith(expected_date), \
        f"Expected order date to start with {expected_date}, got {order['created_at']}"
