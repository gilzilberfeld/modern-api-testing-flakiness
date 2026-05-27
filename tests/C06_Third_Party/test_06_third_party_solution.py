import json
import requests
import respx
from httpx import Response
from pathlib import Path

BASE_URL = "http://localhost:5000"
PAYMENT_SERVICE_URL = "http://localhost:5000/unreliable-payment"


def load_settings_with_fallback():
    config_path = Path(__file__).parent.parent.parent / "config" / "server_config.json"

    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)

    return {
        "server_url": "http://localhost:5000",
        "timeout": 30
    }

def test_load_settings_and_verify_server():
    settings = load_settings_with_fallback()
    server_url = settings.get("server_url", BASE_URL)

    response = requests.get(f"{server_url}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@respx.mock
def test_create_order_with_payment():
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
