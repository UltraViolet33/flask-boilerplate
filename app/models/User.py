from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import func
from datetime import datetime
from .Model import Model
from .. import db
import re


class User(db.Model, Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hashed = db.Column(db.String(200), nullable=False)
    registered_on = db.Column(
        db.DateTime(timezone=True), default=func.now(), nullable=False
    )

    def __init__(self, email, password_plaintext, bypass_pwd=False):
        self.email = email
        self.set_password(password_plaintext, bypass_pwd)
        self.registered_on = datetime.now()

    def set_password(self, password_plaintext, bypass_pwd):
        if not password_plaintext:
            raise AssertionError("Password Missing")
        if bypass_pwd:
            self.password_hashed = generate_password_hash(password_plaintext)
            return
        if len(password_plaintext) < 8 or len(password_plaintext) > 70:
            raise AssertionError("Password length must be between 8 and 50 characters")

        password_pattern = (
            "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        )

        if not re.match(password_pattern, password_plaintext):
            raise AssertionError(
                "Password must contain at least 1 uppercase letter, 1 lowercase letter, 1 number and 1 special character"
            )

        self.password_hashed = generate_password_hash(password_plaintext)

    def is_password_correct(self, password_plaintext):
        return check_password_hash(self.password_hashed, password_plaintext)
