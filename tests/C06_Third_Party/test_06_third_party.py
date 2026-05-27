import json
import requests

BASE_URL = "http://localhost:5000"
CONFIG_FILE = "/etc/bookstore/settings.json"

def test_load_settings_and_verify_server():
    # Assumes The config file may exists
    with open(CONFIG_FILE, "r") as f:
        settings = json.load(f)

    server_url = settings.get("server_url", BASE_URL)

    response = requests.get(f"{server_url}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_order_with_payment():
    # Create an order - server calls payment gateway internally
    order_response = requests.post(f"{BASE_URL}/orders", json={
        "book_id": "book-1",
        "user_id": 1
    })

    assert order_response.status_code == 201, \
        f"Order failed: {order_response.json()}"

    order = order_response.json()
    assert order["status"] == "confirmed"
    assert "transaction_id" in order
