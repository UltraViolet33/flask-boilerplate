from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, current_user, get_jwt
from app.models.User import User
from app.models.TokenBlocklist import TokenBlocklist
from datetime import datetime
from datetime import timezone
from app import db
from app import limiter

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
@limiter.limit("5 per 15 minutes")
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).first()

    if not user or not user.is_password_correct(password):
        return jsonify("Wrong username or password"), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


@auth.route("/register", methods=["POST"])
def register():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if User.query.filter_by(email=email).first():
        return jsonify("Email already in use"), 400

    user = User(email, password)
    user.save()

    return jsonify("User created"), 201


@auth.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(logged_as=current_user.email), 200


@auth.route("/logout", methods=["DELETE"])
@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify(msg="JWT revoked")
