from app.models.User import User    

def test_create_user():
    user = User(email="test@gmail.com", password_plaintext="Password123!")
    assert user.email == "test@gmail.com"
    assert user.password_hashed != "Password123!"


