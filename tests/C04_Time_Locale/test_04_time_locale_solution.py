"""
SUSPECT 4: Time & Locale - STABILIZED SOLUTION

THE FIX: Never compare local time to server time. Use the server's
notion of time, or validate format without asserting specific dates.

Key principles:
1. Use server timestamps, not local datetime.now()
2. Validate format/structure, not specific date values
3. If you need "today", get it from the server
4. Allow tolerance for timing differences
"""

import requests
from datetime import datetime, timezone

BASE_URL = "http://localhost:5000"


def setup_module():
    """Reset server state before tests."""
    requests.post(f"{BASE_URL}/reset")


# =============================================================================
# SOLUTION 1: Use the order's own timestamp to verify it's in "today's" list
# =============================================================================

def test_create_order_appears_in_todays_orders():
    """
    STABILIZED: Instead of assuming what "today" means, we:
    1. Create the order
    2. Extract the server's date from the order's created_at
    3. Verify the order appears in today's orders (server's today, not ours)

    This works regardless of the test machine's timezone.
    """
    # Create an order
    order_response = requests.post(f"{BASE_URL}/orders", json={
        "book_id": "book-1",
        "user_id": 1
    })
    assert order_response.status_code == 201
    created_order = order_response.json()
    order_id = created_order["id"]

    # Parse the server's timestamp to see what date the SERVER thinks it is
    server_timestamp = created_order["created_at"]
    server_date = datetime.fromisoformat(server_timestamp).date()

    # Get today's orders from the server
    todays_response = requests.get(f"{BASE_URL}/orders/today")
    assert todays_response.status_code == 200
    todays_orders = todays_response.json()

    # Now we can reliably check - using the server's notion of "today"
    order_ids = [o["id"] for o in todays_orders]
    assert order_id in order_ids, (
        f"Order {order_id} created at {server_timestamp} (date: {server_date}) "
        f"not found in today's orders"
    )


# =============================================================================
# SOLUTION 2: Validate format, not specific date values
# =============================================================================

def test_order_date_format_is_valid_iso8601():
    """
    STABILIZED: Instead of comparing to local time, we:
    1. Validate the timestamp is valid ISO 8601 format
    2. Validate it's a reasonable timestamp (not in the distant past/future)

    This works regardless of timezone or locale settings.
    """
    # Create an order
    order_response = requests.post(f"{BASE_URL}/orders", json={
        "book_id": "book-2",
        "user_id": 1
    })
    assert order_response.status_code == 201
    order = order_response.json()

    # Validate the timestamp exists and is parseable as ISO 8601
    created_at = order.get("created_at")
    assert created_at is not None, "Order should have created_at field"

    # Parse the timestamp - this validates the format
    try:
        parsed_time = datetime.fromisoformat(created_at)
    except ValueError as e:
        raise AssertionError(f"created_at '{created_at}' is not valid ISO 8601: {e}")

    # Validate it's a reasonable time (within last minute, not in future)
    now_utc = datetime.now(timezone.utc)
    time_diff = abs((now_utc - parsed_time).total_seconds())
    assert time_diff < 60, (
        f"Order timestamp {created_at} differs from current UTC time by {time_diff}s"
    )
