"""
Health and configuration endpoints.
"""

from flask import Blueprint, jsonify
from datetime import datetime, timezone
from src.data import FEATURE_FLAGS

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()})


@health_bp.route("/config", methods=["GET"])
def config():
    """Returns current feature flags - useful for debugging environment issues."""
    return jsonify({"features": FEATURE_FLAGS})
