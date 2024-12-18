from flask import Blueprint, redirect, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, current_user
from app.models.User import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username=username).first()

    if not user or not user.is_password_correct(password):
        return jsonify("Wrong username or password"), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


@auth.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(logged_as=current_user.username), 200


@auth.route("/logout")
def logout():
    return redirect("/login")
