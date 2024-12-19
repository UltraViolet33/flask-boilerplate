from flask_jwt_extended import get_jwt


def test_register_success(test_client):
    response = test_client.post(
        "/register", json={"email": "test@example.com", "password": "Password123!"}
    )
    assert response.status_code == 201
    assert response.get_json() == "User created"


def test_register_duplicate_email(test_client, create_user):
    create_user(email="test@example.com", password="Password123!")

    response = test_client.post(
        "/register", json={"email": "test@example.com", "password": "Password123!s"}
    )
    assert response.status_code == 400
    assert response.get_json() == "Email already in use"


def test_login_success(test_client, create_user):
    create_user(email="test@example.com", password="Password123!")

    response = test_client.post(
        "/login", json={"email": "test@example.com", "password": "Password123!"}
    )
    assert response.status_code == 200
    assert "access_token" in response.get_json()


def test_login_wrong_password(test_client, create_user):
    create_user(email="test@example.com", password="Password123!")

    response = test_client.post(
        "/login", json={"email": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.get_json() == "Wrong username or password"


def test_login_nonexistent_user(test_client):
    response = test_client.post(
        "/login", json={"email": "nonexistent@example.com", "password": "Password123!"}
    )
    assert response.status_code == 401
    assert response.get_json() == "Wrong username or password"


def test_logout_success(test_client, create_user):
    user = create_user(email="test@example.com", password="Password123!")

    login_response = test_client.post(
        "/login", json={"email": "test@example.com", "password": "Password123!"}
    )
    access_token = login_response.get_json()["access_token"]

    response = test_client.delete(
        "/logout", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.get_json()["msg"] == "JWT revoked"

    from app.models.TokenBlocklist import TokenBlocklist

    jti = get_jwt()["jti"]
    token_in_blocklist = TokenBlocklist.query.filter_by(jti=jti).first()
    assert token_in_blocklist is not None
