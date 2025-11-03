from fastapi.testclient import TestClient

from app.limiter import limiter


def test_zzz_rate_limit_user_creation(client: TestClient):
    try:
        limiter.enabled = True
        # The limit is 10 per minute. We'll send 11 requests.
        for i in range(10):
            user_data = {
                "username": f"rate_limit_user_{i}",
                "email": f"rate_limit_{i}@example.com",
                "password": "password123",
            }
            response = client.post("/api/v1/users/", json=user_data)
            assert response.status_code == 200

        # The 11th request should be blocked
        user_data = {
            "username": "rate_limit_user_10",
            "email": "rate_limit_10@example.com",
            "password": "password123",
        }
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 429
    finally:
        limiter.enabled = False
