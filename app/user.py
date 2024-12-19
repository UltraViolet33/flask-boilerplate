from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user


user = Blueprint("user", __name__)


@user.route("/email", methods=["PUT"])
@jwt_required()
def update_email():
    email = request.json.get("email")
    current_user.email = email
    current_user.save()
    return jsonify({"message": "Email updated"}), 200


@user.route("/password", methods=["PUT"])
@jwt_required()
def update_password():
    password = request.json.get("password")
    current_user.set_password(password)
    current_user.save()
    return jsonify({"message": "Password updated"}), 200
