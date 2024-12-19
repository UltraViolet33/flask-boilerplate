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


@pytest.fixture
def log_in_default_user(test_client):
    default_email = "default_user@example.com"
    default_password = "Password123!"

    user = User(email=default_email, password_plaintext=default_password)
    user.save()

    login_response = test_client.post(
        "/login", json={"email": default_email, "password": default_password}
    )

    assert login_response.status_code == 200
    token = login_response.get_json()["access_token"]

    return user, token
