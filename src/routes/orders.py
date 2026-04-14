"""
Orders endpoints.
"""

from flask import Blueprint, jsonify, request, abort
from datetime import datetime, timezone
import httpx
from src import data

orders_bp = Blueprint("orders", __name__)

# External payment service URL
PAYMENT_SERVICE_URL = "http://localhost:5000/unreliable-payment"


def process_payment(amount):
    """
    Calls the external payment gateway service.
    The service is unreliable - fails 30% of the time.
    """
    try:
        response = httpx.post(PAYMENT_SERVICE_URL, json={"amount": amount})
        if response.status_code == 200:
            resp_data = response.json()
            return {"success": True, "transaction_id": resp_data["transaction_id"]}
        else:
            return {"success": False, "error": response.json().get("message", "Payment failed")}
    except httpx.RequestError as e:
        return {"success": False, "error": str(e)}


@orders_bp.route("/orders", methods=["GET"])
def list_orders():
    return jsonify(list(data.orders.values()))


@orders_bp.route("/orders", methods=["POST"])
def create_order():
    req_data = request.get_json()

    if not req_data or "book_id" not in req_data or "user_id" not in req_data:
        abort(400, description="book_id and user_id are required")

    book_id = req_data["book_id"]
    if book_id not in data.books:
        abort(404, description="Book not found")

    book = data.books[book_id]
    if book["stock"] <= 0:
        abort(400, description="Book out of stock")

    price = book["price"]
    user_id = req_data["user_id"]

    # Process payment through external gateway (unreliable!)
    payment_result = process_payment(price)
    if not payment_result["success"]:
        abort(503, description=payment_result["error"])

    # Decrease stock
    data.books[book_id]["stock"] -= 1

    order = {
        "id": data.next_order_id,
        "book_id": book_id,
        "user_id": user_id,
        "price": price,
        "status": "confirmed",
        "transaction_id": payment_result["transaction_id"],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    data.orders[data.next_order_id] = order
    data.next_order_id += 1

    return jsonify(order), 201


@orders_bp.route("/orders/today", methods=["GET"])
def list_todays_orders():
    """Returns orders created today - useful for time/locale tests."""
    today = datetime.now(timezone.utc).date()
    todays_orders = [
        o for o in data.orders.values()
        if datetime.fromisoformat(o["created_at"]).date() == today
    ]
    return jsonify(todays_orders)
