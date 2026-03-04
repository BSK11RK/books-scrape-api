import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)
                    
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200

def test_register_login(client):

    response = client.post(
        "/register",
        params={"username": "testuser", "password": "test123"}
    )
    assert response.status_code == 200

    response = client.post(
        "/login",
        data={"username": "testuser", "password": "test123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_books_requires_auth(client):
    response = client.get("/books")
    assert response.status_code == 401