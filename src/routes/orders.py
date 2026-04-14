"""
Orders endpoints.
"""

from flask import Blueprint, jsonify, request, abort
from datetime import datetime, timezone
from src import data

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/orders", methods=["GET"])
def list_orders():
    return jsonify(list(data.orders.values()))


@orders_bp.route("/orders", methods=["POST"])
def create_order():
    req_data = request.get_json()

    if not req_data or "book_id" not in req_data or "user_id" not in req_data:
        abort(400, description="book_id and user_id are required")

    book_id = req_data["book_id"]  # Now a string (unique_id)
    if book_id not in data.books:
        abort(404, description="Book not found")

    book = data.books[book_id]
    if book["stock"] <= 0:
        abort(400, description="Book out of stock")

    # Calculate price with potential premium discount
    price = book["price"]
    user_id = req_data["user_id"]
    discount_applied = False

    if data.FEATURE_FLAGS["premium_discount"] and user_id in data.users:
        if data.users[user_id].get("is_premium"):
            price = price * 0.9  # 10% discount
            discount_applied = True

    # Decrease stock
    data.books[book_id]["stock"] -= 1

    order = {
        "id": data.next_order_id,
        "book_id": book_id,
        "user_id": user_id,
        "price": price,
        "discount_applied": discount_applied,
        "status": "confirmed",
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
