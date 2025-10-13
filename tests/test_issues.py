from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get_issue():
    r = client.post("/issues", params={"title": "Test Issue"})
    assert r.status_code == 200
    issue = r.json()
    assert "id" in issue
    assert issue["title"] == "Test Issue"
    issue_id = issue["id"]

    r = client.get(f"/issues/{issue_id}")
    assert r.status_code == 200
    issue2 = r.json()
    assert issue == issue2


def test_get_all_issues():
    from app.main import _DB

    _DB["issues"] = []

    client.post("/issues", params={"title": "First"})
    client.post("/issues", params={"title": "Second"})

    r = client.get("/issues")
    assert r.status_code == 200
    body = r.json()
    assert "issues" in body
    assert len(body["issues"]) == 2
