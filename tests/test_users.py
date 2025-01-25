import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_user():
    response = client.post("/users/", json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone_number": "1234567890"
    })
    assert response.status_code == 200
    assert "user_id" in response.json()


def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_user_exists():
    response = client.post("/users/", json={
        "name": "Jane Doe",
        "email": "johndoe@example.com",
        "phone_number": "0987654321"
    })
    assert response.status_code == 200
    assert "message" in response.json()
    assert "User with this email already exists" in response.json()["message"]
