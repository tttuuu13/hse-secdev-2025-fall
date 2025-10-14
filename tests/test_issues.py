def test_create_issue_and_get_it(client):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
    }
    r = client.post("/api/v1/users/", json=user_data)
    assert r.status_code == 200
    user_id = r.json()["id"]
    headers = {"X-User-Id": str(user_id)}

    issue_data = {"title": "Test Issue", "status": "open"}
    r = client.post("/api/v1/issues/", json=issue_data, headers=headers)
    assert r.status_code == 200
    issue = r.json()
    assert issue["title"] == "Test Issue"
    assert issue["owner_id"] == user_id

    r = client.get("/api/v1/issues/", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_update_issue(client):
    user_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "password123",
    }
    r = client.post("/api/v1/users/", json=user_data)
    user_id = r.json()["id"]
    headers = {"X-User-Id": str(user_id)}

    issue_data = {"title": "Initial Title", "status": "open"}
    r = client.post("/api/v1/issues/", json=issue_data, headers=headers)
    issue_id = r.json()["id"]

    update_data = {"title": "Updated Title"}
    r = client.patch(f"/api/v1/issues/{issue_id}", json=update_data, headers=headers)
    assert r.status_code == 200
    assert r.json()["title"] == "Updated Title"


def test_delete_issue(client):
    user_data = {
        "username": "testuser3",
        "email": "test3@example.com",
        "password": "password123",
    }
    r = client.post("/api/v1/users/", json=user_data)
    user_id = r.json()["id"]
    headers = {"X-User-Id": str(user_id)}

    issue_data = {"title": "To Be Deleted", "status": "open"}
    r = client.post("/api/v1/issues/", json=issue_data, headers=headers)
    issue_id = r.json()["id"]

    r = client.delete(f"/api/v1/issues/{issue_id}", headers=headers)
    assert r.status_code == 204

    r = client.get("/api/v1/issues/", headers=headers)
    assert len(r.json()) == 0


def test_read_issue_by_id(client):
    # Create user 1 and their issue
    user1_data = {
        "username": "user1_get",
        "email": "user1_get@example.com",
        "password": "password123",
    }
    r = client.post("/api/v1/users/", json=user1_data)
    user1_id = r.json()["id"]
    headers1 = {"X-User-Id": str(user1_id)}

    issue_data = {"title": "User 1's Issue to Get", "status": "open"}
    r = client.post("/api/v1/issues/", json=issue_data, headers=headers1)
    issue_id = r.json()["id"]

    # User 1 successfully gets their own issue
    r = client.get(f"/api/v1/issues/{issue_id}", headers=headers1)
    assert r.status_code == 200
    assert r.json()["title"] == "User 1's Issue to Get"

    # Check for 404
    r = client.get("/api/v1/issues/9999", headers=headers1)
    assert r.status_code == 404
    assert r.json()["code"] == "NOT_FOUND"

    # Create user 2
    user2_data = {
        "username": "user2_get",
        "email": "user2_get@example.com",
        "password": "password123",
    }
    r = client.post("/api/v1/users/", json=user2_data)
    user2_id = r.json()["id"]
    headers2 = {"X-User-Id": str(user2_id)}

    # User 2 fails to get User 1's issue
    r = client.get(f"/api/v1/issues/{issue_id}", headers=headers2)
    assert r.status_code == 403
    assert r.json()["code"] == "FORBIDDEN"


def test_pagination(client):
    user_data = {
        "username": "pagination_user",
        "email": "pagination@example.com",
        "password": "password123",
    }
    r = client.post("/api/v1/users/", json=user_data)
    user_id = r.json()["id"]
    headers = {"X-User-Id": str(user_id)}

    # Create 5 issues
    for i in range(5):
        issue_data = {"title": f"Issue {i}", "status": "open"}
        client.post("/api/v1/issues/", json=issue_data, headers=headers)

    # Get first page (limit 2)
    r = client.get("/api/v1/issues/?limit=2", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 2
    assert r.json()[0]["title"] == "Issue 0"
    assert r.json()[1]["title"] == "Issue 1"

    # Get second page (limit 2, skip 2)
    r = client.get("/api/v1/issues/?limit=2&skip=2", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 2
    assert r.json()[0]["title"] == "Issue 2"
    assert r.json()[1]["title"] == "Issue 3"

    # Get last page (limit 2, skip 4)
    r = client.get("/api/v1/issues/?limit=2&skip=4", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["title"] == "Issue 4"

    # Get empty page
    r = client.get("/api/v1/issues/?skip=5", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 0
