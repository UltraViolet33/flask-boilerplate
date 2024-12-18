from flask import Blueprint, redirect


auth = Blueprint("auth", __name__)


@auth.route("/", methods=["GET", "POST"])
def login():
    return "login"


@auth.route("/logout")
def logout():
    return redirect("/login")
