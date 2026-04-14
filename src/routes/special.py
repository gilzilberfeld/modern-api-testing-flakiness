"""
Special endpoints for demo purposes.
"""

from flask import Blueprint, jsonify, request, abort
import random
import time
from src import data

special_bp = Blueprint("special", __name__)


@special_bp.route("/slow-search", methods=["GET"])
def slow_search():
    """Simulates a slow external service - for third-party dependency tests."""
    delay = float(request.args.get("delay", 0.5))
    time.sleep(delay)
    return jsonify({"results": ["Book A", "Book B"], "delay": delay})


@special_bp.route("/unreliable-payment", methods=["POST"])
def unreliable_payment():
    """Simulates an unreliable payment gateway - randomly fails."""
    if random.random() < 0.3:  # 30% failure rate
        abort(503, description="Payment gateway temporarily unavailable")
    return jsonify({"status": "approved", "transaction_id": f"TXN-{random.randint(1000, 9999)}"})


@special_bp.route("/ai/recommend", methods=["POST"])
def ai_recommend():
    """Simulates an AI recommendation endpoint - returns varied responses."""
    req_data = request.get_json() or {}
    genre = req_data.get("genre", "fiction")

    # Simulate AI non-determinism: different responses for same input
    recommendations = [
        f"Based on your interest in {genre}, I recommend 'The Great Gatsby'",
        f"For {genre} lovers, try 'To Kill a Mockingbird'",
        f"You might enjoy '1984' - a classic {genre} choice",
        f"Consider 'Pride and Prejudice' for your {genre} reading",
    ]

    return jsonify({
        "recommendation": random.choice(recommendations),
        "confidence": round(random.uniform(0.7, 0.99), 2),
    })


@special_bp.route("/reset", methods=["POST"])
def reset_data():
    """Resets all data to initial state - useful for test cleanup."""
    data.books.clear()
    data.books.update(data.INITIAL_BOOKS)
    data.users.clear()
    data.next_user_id = 1
    data.reviews.clear()
    data.next_review_id = 1
    data.orders.clear()
    data.next_order_id = 1

    return jsonify({"status": "reset complete"})
