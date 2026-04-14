"""
Users endpoints.
"""

from flask import Blueprint, jsonify, request, abort
from datetime import datetime, timezone
from src import data

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["GET"])
def list_users():
    return jsonify(list(data.users.values()))


@users_bp.route("/users", methods=["POST"])
def create_user():
    req_data = request.get_json()

    if not req_data or "email" not in req_data:
        abort(400, description="Email is required")

    # Check for duplicate email
    for user in data.users.values():
        if user["email"] == req_data["email"]:
            abort(409, description=f"User with email {req_data['email']} already exists")

    user = {
        "id": data.next_user_id,
        "email": req_data["email"],
        "name": req_data.get("name", ""),
        "is_premium": req_data.get("is_premium", False),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    data.users[data.next_user_id] = user
    data.next_user_id += 1

    return jsonify(user), 201


@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    if user_id not in data.users:
        abort(404, description="User not found")
    return jsonify(data.users[user_id])


@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in data.users:
        abort(404, description="User not found")
    del data.users[user_id]
    return "", 204
