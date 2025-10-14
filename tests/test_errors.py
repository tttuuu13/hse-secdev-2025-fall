def test_duplicate_user_email(client):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password",
    }
    client.post("/users/", json=user_data)
    r = client.post("/users/", json=user_data)
    assert r.status_code == 400
    assert r.json() == {"detail": "Email already registered"}
