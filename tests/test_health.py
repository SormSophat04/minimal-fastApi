from tests.conftest import get_client


def test_root_and_health():
    client = get_client()
    try:
        assert client.get("/").status_code == 200
        r = client.get("/api/v1/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok", "database": "connected"}
    finally:
        client.__exit__(None, None, None)
