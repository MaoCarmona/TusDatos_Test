import pytest
from fastapi.testclient import TestClient
from database.database import load_json_db
from main import app

processes = load_json_db()

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

class TestGetProcess:
    @pytest.mark.asyncio
    async def test_default_limit_and_offset(self, client):
        # Make login request to obtain token
        login_response = client.post("/api/login", json={"username": "Mauricio Camona", "email": "example@example.com"})
        assert login_response.status_code == 200
        token = login_response.json()["token"]

        # Make GET request to /api/process with token in authorization header
        response = client.get("/api/process", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json() == processes[:10]

    @pytest.mark.asyncio
    async def test_empty_processes(self, client):
        # Make login request to obtain token
        login_response = client.post("/api/login", json={"username": "Mauricio Camona", "email": "example@example.com"})
        assert login_response.status_code == 200
        token = login_response.json()["token"]

        # Clear the processes list and then make GET request to /api/process with token in authorization header
        processes.clear()
        response = client.get("/api/process", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json() == []
