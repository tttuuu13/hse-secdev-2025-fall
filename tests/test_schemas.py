from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_user_invalid_email():
    user_data = {
        "username": "testuser",
        "email": "invalid-email",
        "password": "password123",
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 422
    response_json = response.json()
    assert response_json["detail"][0]["loc"] == ["body", "email"]
    assert "valid email address" in response_json["detail"][0]["msg"]
    assert "correlation_id" in response_json
    assert response_json["title"] == "Validation Error"
    assert response_json["status"] == 422


def test_create_user_short_password():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "short",
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 422
    response_json = response.json()
    assert response_json["detail"][0]["loc"] == ["body", "password"]
    assert (
        response_json["detail"][0]["msg"] == "String should have at least 8 characters"
    )
    assert "correlation_id" in response_json
    assert response_json["title"] == "Validation Error"
    assert response_json["status"] == 422


def test_create_issue_empty_title():
    user_data = {
        "username": "issueuser",
        "email": "issue@example.com",
        "password": "password123",
    }
    r = client.post("/api/v1/users/", json=user_data)
    user_id = r.json()["id"]
    headers = {"X-User-Id": str(user_id)}

    issue_data = {"title": "", "status": "open"}
    response = client.post("/api/v1/issues/", json=issue_data, headers=headers)
    assert response.status_code == 422
    response_json = response.json()
    assert response_json["detail"][0]["loc"] == ["body", "title"]
    assert (
        response_json["detail"][0]["msg"] == "String should have at least 1 character"
    )
    assert "correlation_id" in response_json
    assert response_json["title"] == "Validation Error"
    assert response_json["status"] == 422


def test_create_issue_long_title():
    user_data = {
        "username": "issueuser2",
        "email": "issue2@example.com",
        "password": "password123",
    }
    r = client.post("/api/v1/users/", json=user_data)
    user_id = r.json()["id"]
    headers = {"X-User-Id": str(user_id)}

    long_title = "a" * 256
    issue_data = {"title": long_title, "status": "open"}
    response = client.post("/api/v1/issues/", json=issue_data, headers=headers)
    assert response.status_code == 422
    response_json = response.json()
    assert response_json["detail"][0]["loc"] == ["body", "title"]
    assert (
        response_json["detail"][0]["msg"] == "String should have at most 255 characters"
    )
    assert "correlation_id" in response_json
    assert response_json["title"] == "Validation Error"
    assert response_json["status"] == 422


def test_create_user_long_password():
    user_data = {
        "username": "longpassuser",
        "email": "longpass@example.com",
        "password": "a" * 129,
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 422
    response_json = response.json()
    assert response_json["detail"][0]["loc"] == ["body", "password"]
    assert (
        response_json["detail"][0]["msg"] == "String should have at most 128 characters"
    )
    assert "correlation_id" in response_json
    assert response_json["title"] == "Validation Error"
    assert response_json["status"] == 422


def test_create_label_empty_name():
    user_data = {
        "username": "labeluser",
        "email": "label@example.com",
        "password": "password123",
    }
    r = client.post("/api/v1/users/", json=user_data)
    user_id = r.json()["id"]
    headers = {"X-User-Id": str(user_id)}

    label_data = {"name": ""}
    response = client.post("/api/v1/labels/", json=label_data, headers=headers)
    assert response.status_code == 422
    response_json = response.json()
    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert (
        response_json["detail"][0]["msg"] == "String should have at least 1 character"
    )
    assert "correlation_id" in response_json
    assert response_json["title"] == "Validation Error"
    assert response_json["status"] == 422


def test_create_label_long_name():
    user_data = {
        "username": "labeluser2",
        "email": "label2@example.com",
        "password": "password123",
    }
    r = client.post("/api/v1/users/", json=user_data)
    user_id = r.json()["id"]
    headers = {"X-User-Id": str(user_id)}

    long_name = "b" * 101
    label_data = {"name": long_name}
    response = client.post("/api/v1/labels/", json=label_data, headers=headers)
    assert response.status_code == 422
    response_json = response.json()
    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert (
        response_json["detail"][0]["msg"] == "String should have at most 100 characters"
    )
    assert "correlation_id" in response_json
    assert response_json["title"] == "Validation Error"
    assert response_json["status"] == 422
