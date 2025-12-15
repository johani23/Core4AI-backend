from flask import Blueprint, jsonify, request

users_bp = Blueprint("users", __name__)

# Mock DB
users = [
    {"id": 1, "name": "Ahmed", "cluster_id": 1, "friends": [2]},
    {"id": 2, "name": "Sama", "cluster_id": 1, "friends": [1]},
    {"id": 3, "name": "Noor", "cluster_id": 2, "friends": []},
]

@users_bp.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@users_bp.route("/api/friends/<int:user_id>", methods=["GET"])
def get_friends(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    friends = [u for u in users if u["id"] in user["friends"]]
    return jsonify(friends)

@users_bp.route("/api/friends/add", methods=["POST"])
def add_friend():
    data = request.json
    user_id = data.get("user_id")
    friend_id = data.get("friend_id")

    user = next((u for u in users if u["id"] == user_id), None)
    friend = next((u for u in users if u["id"] == friend_id), None)

    if not user or not friend:
        return jsonify({"error": "User not found"}), 404

    if friend_id not in user["friends"]:
        user["friends"].append(friend_id)
    if user_id not in friend["friends"]:
        friend["friends"].append(user_id)

    return jsonify({"message": "Friend added successfully"})
