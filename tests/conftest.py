import pytest
from app import create_app, db
from app.models.User import User


@pytest.fixture
def test_client():
    app = create_app("config.TestingConfig")
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


@pytest.fixture
def create_user():
    def _create_user(email, password):
        user = User(email=email, password_plaintext=password)
        user.save()
        return user

    return _create_user
