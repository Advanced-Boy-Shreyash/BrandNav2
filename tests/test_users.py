from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add_user():
    # Test adding a new user
    response = client.post("/users/", json={
        "name": "John Doe",
        "email": "john@example.com",
        "phone_number": "1234567890"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "User added successfully"}

def test_get_users():
    # Test getting all users
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)

def test_add_duplicate_user():
    # Test adding a duplicate user
    response = client.post("/users/", json={
        "name": "John Doe",
        "email": "john@example.com",
        "phone_number": "1234567890"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "User with this email already exists."}