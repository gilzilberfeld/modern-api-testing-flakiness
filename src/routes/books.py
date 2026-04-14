"""
Books endpoints.
"""

from flask import Blueprint, jsonify, request, abort
from datetime import datetime, timezone
import os
import httpx
from src import data

books_bp = Blueprint("books", __name__)

# Gemini API configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


def lookup_author_with_llm(title):
    """
    Calls Gemini to look up the author of a book.

    LLMs are non-deterministic - they return different phrasings
    for the same question, especially for books with multiple authors.
    """
    if not GEMINI_API_KEY:
        return "Unknown Author (No API key)"

    prompt = f"Who is the author of the book '{title}'? Reply with just the author name(s), nothing else."

    try:
        response = httpx.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            json={
                "contents": [{"parts": [{"text": prompt}]}]
            },
            timeout=10.0
        )

        if response.status_code == 200:
            data = response.json()
            # Extract text from Gemini response
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return text.strip()
        else:
            return f"Unknown Author (API error: {response.status_code})"

    except httpx.RequestError as e:
        return f"Unknown Author (Request error: {e})"


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


@books_bp.route("/books/auto", methods=["POST"])
def create_book_with_llm():
    """
    Creates a book with just a title - uses LLM to look up the author.

    This endpoint demonstrates AI indeterminacy: the LLM returns
    different author formats for the same book title.
    """
    req_data = request.get_json()

    if not req_data or "title" not in req_data:
        abort(400, description="Title is required")

    if "unique_id" not in req_data:
        abort(400, description="unique_id is required")

    unique_id = req_data["unique_id"]

    if unique_id in data.books:
        abort(409, description=f"Book with unique_id {unique_id} already exists")

    # Use LLM to look up the author (non-deterministic!)
    author = lookup_author_with_llm(req_data["title"])

    book = {
        "unique_id": unique_id,
        "title": req_data["title"],
        "author": author,
        "price": req_data.get("price", 0.0),
        "stock": req_data.get("stock", 0),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    data.books[unique_id] = book

    return jsonify(book), 201
