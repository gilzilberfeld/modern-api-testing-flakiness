"""
Bigger Better Bookstore API

A simple Flask API for demonstrating flaky test patterns.
Uses in-memory storage - data resets when the server restarts.
"""

from flask import Flask, jsonify
import os
import sys

# Add parent directory to path for direct script execution
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

# Register blueprints
from src.routes.health import health_bp
from src.routes.books import books_bp
from src.routes.reviews import reviews_bp
from src.routes.orders import orders_bp
from src.routes.special import special_bp

app.register_blueprint(health_bp)
app.register_blueprint(books_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(special_bp)


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
