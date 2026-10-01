from tests.conftest import get_client


def test_user_crud():
    client = get_client()
    try:
        created = client.post("/api/v1/users", json={"name": "Ada", "email": "ada@example.com"})
        assert created.status_code == 201, created.text
        user_id = created.json()["id"]

        duplicate = client.post("/api/v1/users", json={"name": "Ada", "email": "ada@example.com"})
        assert duplicate.status_code == 400

        listed = client.get("/api/v1/users")
        assert listed.status_code == 200
        assert len(listed.json()) >= 1

        fetched = client.get(f"/api/v1/users/{user_id}")
        assert fetched.status_code == 200

        deleted = client.delete(f"/api/v1/users/{user_id}")
        assert deleted.status_code == 200
        assert deleted.json() == {"deleted": True, "id": user_id}

        missing = client.get(f"/api/v1/users/{user_id}")
        assert missing.status_code == 404
    finally:
        client.__exit__(None, None, None)
