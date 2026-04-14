"""
Reviews endpoints.
"""

from flask import Blueprint, jsonify, request, abort
from datetime import datetime, timezone
from src import data

reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.route("/books/<book_id>/reviews", methods=["GET"])
def list_reviews(book_id):
    if book_id not in data.books:
        abort(404, description="Book not found")
    book_reviews = [r for r in data.reviews.values() if r["book_id"] == book_id]
    return jsonify(book_reviews)


@reviews_bp.route("/books/<book_id>/reviews", methods=["POST"])
def create_review(book_id):
    if book_id not in data.books:
        abort(404, description="Book not found")

    req_data = request.get_json()
    if not req_data or "rating" not in req_data:
        abort(400, description="Rating is required")

    # Feature flag: review moderation
    status = "pending" if data.FEATURE_FLAGS["review_moderation"] else "approved"

    review = {
        "id": data.next_review_id,
        "book_id": book_id,
        "user_id": req_data.get("user_id"),
        "rating": req_data["rating"],
        "comment": req_data.get("comment", ""),
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    data.reviews[data.next_review_id] = review
    data.next_review_id += 1

    return jsonify(review), 201
