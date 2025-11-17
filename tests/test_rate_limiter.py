from fastapi.testclient import TestClient

from app.limiter import limiter


def test_zzz_rate_limit_user_creation(client: TestClient):
    try:
        limiter.enabled = True
        # The limit is 100 per minute. We'll send 101 requests.
        for i in range(100):
            user_data = {
                "username": f"rate_limit_user_{i}",
                "email": f"rate_limit_{i}@example.com",
                "password": "password123",
            }
            response = client.post("/api/v1/users/", json=user_data)
            assert response.status_code == 200

        # The 101st request should be blocked
        user_data = {
            "username": "rate_limit_user_100",
            "email": "rate_limit_100@example.com",
            "password": "password123",
        }
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 429
        response_json = response.json()
        assert response_json["title"] == "Too Many Requests"
        assert response_json["status"] == 429
        assert "correlation_id" in response_json
        assert "Retry-After" in response.headers
    finally:
        limiter.enabled = False
