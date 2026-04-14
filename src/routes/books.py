"""
Books endpoints.
"""

from flask import Blueprint, jsonify, request, abort
from datetime import datetime, timezone
from src import data

books_bp = Blueprint("books", __name__)


@books_bp.route("/books", methods=["GET"])
def list_books():
    return jsonify(list(data.books.values()))


@books_bp.route("/books/<book_id>", methods=["GET"])
def get_book(book_id):
    if book_id not in data.books:
        abort(404, description="Book not found")
    return jsonify(data.books[book_id])


@books_bp.route("/books", methods=["POST"])
def create_book():
    req_data = request.get_json()

    if not req_data or "title" not in req_data:
        abort(400, description="Title is required")

    if "unique_id" not in req_data:
        abort(400, description="unique_id is required")

    unique_id = req_data["unique_id"]

    # Check for duplicate unique_id
    if unique_id in data.books:
        abort(409, description=f"Book with unique_id {unique_id} already exists")

    book = {
        "unique_id": unique_id,
        "title": req_data["title"],
        "author": req_data.get("author", "Unknown"),
        "price": req_data.get("price", 0.0),
        "stock": req_data.get("stock", 0),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    data.books[unique_id] = book

    return jsonify(book), 201


@books_bp.route("/books/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    if book_id not in data.books:
        abort(404, description="Book not found")
    del data.books[book_id]
    return "", 204


@books_bp.route("/books/count", methods=["GET"])
def count_books():
    """Returns the total count of books - useful for concurrency tests."""
    return jsonify({"count": len(data.books)})
