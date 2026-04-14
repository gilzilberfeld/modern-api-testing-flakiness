"""
Bigger Better Bookstore API

A simple Flask API for demonstrating flaky test patterns.
Uses in-memory storage - data resets when the server restarts.
"""

from flask import Flask, jsonify, request, abort
from datetime import datetime, timezone
import os
import random
import time

app = Flask(__name__)

# =============================================================================
# IN-MEMORY DATA STORE
# =============================================================================

# Books catalog (keyed by unique_id string)
books = {
    "book-1": {"unique_id": "book-1", "title": "The Pragmatic Programmer", "author": "Hunt & Thomas", "price": 49.99, "stock": 10},
    "book-2": {"unique_id": "book-2", "title": "Clean Code", "author": "Robert Martin", "price": 39.99, "stock": 5},
    "book-3": {"unique_id": "book-3", "title": "Design Patterns", "author": "Gang of Four", "price": 59.99, "stock": 3},
}

# Registered users
users = {}
next_user_id = 1

# Book reviews
reviews = {}
next_review_id = 1

# Orders
orders = {}
next_order_id = 1

# Feature flags (for Suspect 5: Environment & Configuration)
FEATURE_FLAGS = {
    "premium_discount": os.environ.get("FEATURE_PREMIUM_DISCOUNT", "false").lower() == "true",
    "review_moderation": os.environ.get("FEATURE_REVIEW_MODERATION", "false").lower() == "true",
}


# =============================================================================
# HEALTH & INFO
# =============================================================================

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()})


@app.route("/config", methods=["GET"])
def config():
    """Returns current feature flags - useful for debugging environment issues."""
    return jsonify({"features": FEATURE_FLAGS})


# =============================================================================
# BOOKS ENDPOINTS
# =============================================================================

@app.route("/books", methods=["GET"])
def list_books():
    return jsonify(list(books.values()))


@app.route("/books/<book_id>", methods=["GET"])
def get_book(book_id):
    if book_id not in books:
        abort(404, description="Book not found")
    return jsonify(books[book_id])


@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()

    if not data or "title" not in data:
        abort(400, description="Title is required")

    if "unique_id" not in data:
        abort(400, description="unique_id is required")

    unique_id = data["unique_id"]

    # Check for duplicate unique_id
    if unique_id in books:
        abort(409, description=f"Book with unique_id {unique_id} already exists")

    book = {
        "unique_id": unique_id,
        "title": data["title"],
        "author": data.get("author", "Unknown"),
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    books[unique_id] = book

    return jsonify(book), 201


@app.route("/books/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    if book_id not in books:
        abort(404, description="Book not found")
    del books[book_id]
    return "", 204


@app.route("/books/count", methods=["GET"])
def count_books():
    """Returns the total count of books - useful for concurrency tests."""
    return jsonify({"count": len(books)})


# =============================================================================
# USERS ENDPOINTS
# =============================================================================

@app.route("/users", methods=["GET"])
def list_users():
    return jsonify(list(users.values()))


@app.route("/users", methods=["POST"])
def create_user():
    global next_user_id
    data = request.get_json()

    if not data or "email" not in data:
        abort(400, description="Email is required")

    # Check for duplicate email
    for user in users.values():
        if user["email"] == data["email"]:
            abort(409, description=f"User with email {data['email']} already exists")

    user = {
        "id": next_user_id,
        "email": data["email"],
        "name": data.get("name", ""),
        "is_premium": data.get("is_premium", False),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    users[next_user_id] = user
    next_user_id += 1

    return jsonify(user), 201


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    if user_id not in users:
        abort(404, description="User not found")
    return jsonify(users[user_id])


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        abort(404, description="User not found")
    del users[user_id]
    return "", 204


# =============================================================================
# REVIEWS ENDPOINTS
# =============================================================================

@app.route("/books/<book_id>/reviews", methods=["GET"])
def list_reviews(book_id):
    if book_id not in books:
        abort(404, description="Book not found")
    book_reviews = [r for r in reviews.values() if r["book_id"] == book_id]
    return jsonify(book_reviews)


@app.route("/books/<book_id>/reviews", methods=["POST"])
def create_review(book_id):
    global next_review_id

    if book_id not in books:
        abort(404, description="Book not found")

    data = request.get_json()
    if not data or "rating" not in data:
        abort(400, description="Rating is required")

    # Feature flag: review moderation
    status = "pending" if FEATURE_FLAGS["review_moderation"] else "approved"

    review = {
        "id": next_review_id,
        "book_id": book_id,
        "user_id": data.get("user_id"),
        "rating": data["rating"],
        "comment": data.get("comment", ""),
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    reviews[next_review_id] = review
    next_review_id += 1

    return jsonify(review), 201


# =============================================================================
# ORDERS ENDPOINTS
# =============================================================================

@app.route("/orders", methods=["GET"])
def list_orders():
    return jsonify(list(orders.values()))


@app.route("/orders", methods=["POST"])
def create_order():
    global next_order_id
    data = request.get_json()

    if not data or "book_id" not in data or "user_id" not in data:
        abort(400, description="book_id and user_id are required")

    book_id = data["book_id"]  # Now a string (unique_id)
    if book_id not in books:
        abort(404, description="Book not found")

    book = books[book_id]
    if book["stock"] <= 0:
        abort(400, description="Book out of stock")

    # Calculate price with potential premium discount
    price = book["price"]
    user_id = data["user_id"]
    discount_applied = False

    if FEATURE_FLAGS["premium_discount"] and user_id in users:
        if users[user_id].get("is_premium"):
            price = price * 0.9  # 10% discount
            discount_applied = True

    # Decrease stock
    books[book_id]["stock"] -= 1

    order = {
        "id": next_order_id,
        "book_id": book_id,
        "user_id": user_id,
        "price": price,
        "discount_applied": discount_applied,
        "status": "confirmed",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    orders[next_order_id] = order
    next_order_id += 1

    return jsonify(order), 201


@app.route("/orders/today", methods=["GET"])
def list_todays_orders():
    """Returns orders created today - useful for time/locale tests."""
    today = datetime.now(timezone.utc).date()
    todays_orders = [
        o for o in orders.values()
        if datetime.fromisoformat(o["created_at"]).date() == today
    ]
    return jsonify(todays_orders)


# =============================================================================
# SPECIAL ENDPOINTS FOR DEMO PURPOSES
# =============================================================================

@app.route("/slow-search", methods=["GET"])
def slow_search():
    """Simulates a slow external service - for third-party dependency tests."""
    delay = float(request.args.get("delay", 0.5))
    time.sleep(delay)
    return jsonify({"results": ["Book A", "Book B"], "delay": delay})


@app.route("/unreliable-payment", methods=["POST"])
def unreliable_payment():
    """Simulates an unreliable payment gateway - randomly fails."""
    if random.random() < 0.3:  # 30% failure rate
        abort(503, description="Payment gateway temporarily unavailable")
    return jsonify({"status": "approved", "transaction_id": f"TXN-{random.randint(1000, 9999)}"})


@app.route("/ai/recommend", methods=["POST"])
def ai_recommend():
    """Simulates an AI recommendation endpoint - returns varied responses."""
    data = request.get_json() or {}
    genre = data.get("genre", "fiction")

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


@app.route("/reset", methods=["POST"])
def reset_data():
    """Resets all data to initial state - useful for test cleanup."""
    global books, users, reviews, orders
    global next_user_id, next_review_id, next_order_id

    books = {
        "book-1": {"unique_id": "book-1", "title": "The Pragmatic Programmer", "author": "Hunt & Thomas", "price": 49.99, "stock": 10},
        "book-2": {"unique_id": "book-2", "title": "Clean Code", "author": "Robert Martin", "price": 39.99, "stock": 5},
        "book-3": {"unique_id": "book-3", "title": "Design Patterns", "author": "Gang of Four", "price": 59.99, "stock": 3},
    }
    users = {}
    next_user_id = 1
    reviews = {}
    next_review_id = 1
    orders = {}
    next_order_id = 1

    return jsonify({"status": "reset complete"})


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": str(error.description)}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": str(error.description)}), 404


@app.errorhandler(409)
def conflict(error):
    return jsonify({"error": "Conflict", "message": str(error.description)}), 409


@app.errorhandler(503)
def service_unavailable(error):
    return jsonify({"error": "Service Unavailable", "message": str(error.description)}), 503


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
