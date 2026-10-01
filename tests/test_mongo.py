from tests.conftest import get_client


def test_mongo_health_and_notes_crud():
    client = get_client()
    try:
        health = client.get("/api/v1/mongo/health")
        assert health.status_code == 200, health.text
        assert health.json()["status"] == "ok"

        created = client.post(
            "/api/v1/mongo/notes", json={"title": "hello mongo", "content": "local test"}
        )
        assert created.status_code == 201, created.text
        note_id = created.json()["id"]

        listed = client.get("/api/v1/mongo/notes")
        assert listed.status_code == 200
        assert any(n["id"] == note_id for n in listed.json())

        fetched = client.get(f"/api/v1/mongo/notes/{note_id}")
        assert fetched.status_code == 200

        deleted = client.delete(f"/api/v1/mongo/notes/{note_id}")
        assert deleted.status_code == 200
        assert deleted.json() == {"deleted": True, "id": note_id}

        missing = client.get(f"/api/v1/mongo/notes/{note_id}")
        assert missing.status_code == 404
    finally:
        client.__exit__(None, None, None)
