import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_book():
    response = client.post("/books/", json={
        "id": 1,
        "title": "Test Book",
        "author": "Test Author",
        "genre": "Fiction",
        "publication_year": 2022
    })
    assert response.status_code == 200
    assert "book_id" in response.json()


def test_get_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_books_with_filter():
    response = client.get("/books/?author=Test Author&genre=Fiction")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_no_books_found():
    response = client.get("/books/?author=Non-existent")
    assert response.status_code == 404
    assert "No books found" in response.json()["detail"]
