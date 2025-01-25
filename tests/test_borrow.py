import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_borrow_book():
    response = client.post("/borrow/", json={
        "id": 1,
        "return_date": "2025-04-02",
        "book_id": 1,
        "user_id": 1,
        "borrow_date": "2025-01-01",
        "is_returned": "false"
    })
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Book borrowed successfully"


def test_borrow_book_already_borrowed():
    response = client.post("/borrow/", json={
        "book_id": 1,
        "user_id": 1,
        "borrow_date": "2025-01-01"
    })
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Book is already borrowed"


def test_return_book():
    response = client.post("/borrow/return/", json={
        "record_id": 1
    })
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Book returned successfully"


def test_return_book_not_borrowed():
    response = client.post("/borrow/return/", json={
        "record_id": 999  # Non-existent record
    })
    assert response.status_code == 404
    assert "message" in response.json()
    assert response.json()["message"] == "Borrow record not found"
