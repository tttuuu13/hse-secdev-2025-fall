def test_create_and_get_issue(client):
    # First, create a user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password",
    }
    r = client.post("/users/", json=user_data)
    assert r.status_code == 200
    user = r.json()
    user_id = user["id"]

    # Now, create an issue for that user
    issue_data = {"title": "Test Issue", "status": "open"}
    r = client.post(f"/users/{user_id}/issues/", json=issue_data)
    assert r.status_code == 200
    issue = r.json()
    assert "id" in issue
    assert issue["title"] == "Test Issue"
    assert issue["owner_id"] == user_id


def test_get_all_issues(client):
    # Create a user and some issues
    user_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "password",
    }
    r = client.post("/users/", json=user_data)
    user_id = r.json()["id"]
    client.post(f"/users/{user_id}/issues/", json={"title": "First", "status": "open"})
    client.post(
        f"/users/{user_id}/issues/", json={"title": "Second", "status": "closed"}
    )

    r = client.get("/issues/")
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list)
    assert len(body) == 2
