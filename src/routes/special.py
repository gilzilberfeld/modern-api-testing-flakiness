"""
Special endpoints for demo purposes.
"""

from flask import Blueprint, jsonify, request, abort
import random
from src import data

special_bp = Blueprint("special", __name__)


@special_bp.route("/unreliable-payment", methods=["POST"])
def unreliable_payment():
    """Simulates an unreliable payment gateway - randomly fails 30% of the time."""
    if random.random() < 0.3:
        abort(503, description="Payment gateway temporarily unavailable")
    return jsonify({"status": "approved", "transaction_id": f"TXN-{random.randint(1000, 9999)}"})


@special_bp.route("/reset", methods=["POST"])
def reset_data():
    """Resets all data to initial state - useful for test cleanup."""
    data.books.clear()
    data.books.update(data.INITIAL_BOOKS)
    data.reviews.clear()
    data.next_review_id = 1
    data.orders.clear()
    data.next_order_id = 1

    return jsonify({"status": "reset complete"})
