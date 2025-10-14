def test_unauthorized_access(client):
    # No X-User-Id header - this still raises a default HTTPException
    r = client.get("/api/v1/issues/")
    assert r.status_code == 401
    assert r.json() == {"detail": "X-User-Id header missing"}


def test_user_not_found(client):
    headers = {"X-User-Id": "9999"}
    r = client.get("/api/v1/issues/", headers=headers)
    assert r.status_code == 404
    assert r.json()["code"] == "NOT_FOUND"


def test_owner_only_access(client):
    # Create user 1 and their issue
    user1_data = {
        "username": "user1",
        "email": "user1@example.com",
        "password": "password123",
    }
    r = client.post("/api/v1/users/", json=user1_data)
    user1_id = r.json()["id"]
    headers1 = {"X-User-Id": str(user1_id)}

    issue_data = {"title": "User 1's Issue", "status": "open"}
    r = client.post("/api/v1/issues/", json=issue_data, headers=headers1)
    issue_id = r.json()["id"]

    # Create user 2
    user2_data = {
        "username": "user2",
        "email": "user2@example.com",
        "password": "password123",
    }
    r = client.post("/api/v1/users/", json=user2_data)
    user2_id = r.json()["id"]
    headers2 = {"X-User-Id": str(user2_id)}

    # User 2 tries to patch User 1's issue
    update_data = {"title": "Hacked"}
    r = client.patch(f"/api/v1/issues/{issue_id}", json=update_data, headers=headers2)
    assert r.status_code == 403
    assert r.json()["code"] == "FORBIDDEN"

    # User 2 tries to delete User 1's issue
    r = client.delete(f"/api/v1/issues/{issue_id}", headers=headers2)
    assert r.status_code == 403
    assert r.json()["code"] == "FORBIDDEN"


def test_admin_override(client, session):
    # Create user 1 and their issue
    user1_data = {
        "username": "user1_admin_test",
        "email": "user1_admin@example.com",
        "password": "password123",
    }
    r = client.post("/api/v1/users/", json=user1_data)
    user1_id = r.json()["id"]
    headers1 = {"X-User-Id": str(user1_id)}

    issue_data = {"title": "User 1's Issue for Admin", "status": "open"}
    r = client.post("/api/v1/issues/", json=issue_data, headers=headers1)
    issue_id = r.json()["id"]

    # Create admin user
    admin_data = {
        "username": "admin_user",
        "email": "admin@example.com",
        "password": "password123",
    }
    r = client.post("/api/v1/users/", json=admin_data)
    admin_id = r.json()["id"]
    headers_admin = {"X-User-Id": str(admin_id)}

    # Manually set the user role to admin in DB
    from app.domain import models

    db_admin = session.query(models.User).filter(models.User.id == admin_id).first()
    db_admin.role = "admin"
    session.commit()
    session.refresh(db_admin)

    # Admin can read user 1's issue
    r = client.get(f"/api/v1/issues/{issue_id}", headers=headers_admin)
    assert r.status_code == 200

    # Admin can update user 1's issue
    update_data = {"title": "Admin Was Here"}
    r = client.patch(
        f"/api/v1/issues/{issue_id}", json=update_data, headers=headers_admin
    )
    assert r.status_code == 200
    assert r.json()["title"] == "Admin Was Here"

    # Admin can delete user 1's issue
    r = client.delete(f"/api/v1/issues/{issue_id}", headers=headers_admin)
    assert r.status_code == 204


def test_duplicate_email(client):
    user1_data = {
        "username": "user1_dup",
        "email": "duplicate@example.com",
        "password": "password123",
    }
    client.post("/api/v1/users/", json=user1_data)

    user2_data = {
        "username": "user2_dup",
        "email": "duplicate@example.com",
        "password": "password123",
    }
    r = client.post("/api/v1/users/", json=user2_data)
    assert r.status_code == 409
    assert r.json()["code"] == "CONFLICT"
