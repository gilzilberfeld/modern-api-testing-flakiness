import requests
from datetime import datetime, timezone

BASE_URL = "http://localhost:5000"


def setup_module():
    requests.post(f"{BASE_URL}/reset")

def test_create_order_appears_in_today_orders():
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

    today_response = requests.get(f"{BASE_URL}/orders/today")
    assert today_response.status_code == 200
    today_orders = today_response.json()

    # Now we can reliably check - using the server's notion of "today"
    order_ids = [o["id"] for o in today_orders]
    assert order_id in order_ids, (
        f"Order {order_id} created at {server_timestamp} (date: {server_date}) "
        f"not found in today's orders"
    )


def test_order_date_format_matches_expected():
    order_response = requests.post(f"{BASE_URL}/orders", json={
        "book_id": "book-2",
        "user_id": 1
    })
    assert order_response.status_code == 201
    order = order_response.json()

    created_at = order.get("created_at")
    try:
        parsed_time = datetime.fromisoformat(created_at)
    except ValueError as e:
        raise AssertionError(f"created_at '{created_at}' is not valid ISO 8601: {e}")

    now_utc = datetime.now(timezone.utc)
    time_diff = abs((now_utc - parsed_time).total_seconds())
    assert time_diff < 60, (
        f"Order timestamp {created_at} differs from current UTC time by {time_diff}s"
    )
