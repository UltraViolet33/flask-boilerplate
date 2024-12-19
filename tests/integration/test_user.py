def test_user_set_email(test_client, log_in_default_user):
    user, token = log_in_default_user

    test_client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"

    new_email = "test2@example.com"
    response = test_client.put("/user/email", json={"email": new_email})

    assert response.status_code == 200
    assert response.get_json() == {"message": "Email updated"}
    assert user.email == new_email


def test_user_set_password(test_client, log_in_default_user):
    user, token = log_in_default_user

    test_client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"

    new_password = "NewPassword123!"
    response = test_client.put("/user/password", json={"password": new_password})

    assert response.status_code == 200
    assert response.get_json() == {"message": "Password updated"}
    assert user.is_password_correct(new_password)
