from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add_book():
    # Test adding a new book
    response = client.post("/books/", json={
        "title": "Test Book",
        "author": "Test Author",
        "genre": "Fiction",
        "publication_year": 2021
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Book added successfully"}

def test_get_books():
    # Test getting all books
    response = client.get("/books/")
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, list)

def test_get_books_by_author():
    # Test getting books by author
    response = client.get("/books/?author=Test Author")
    assert response.status_code == 200
    books = response.json()
    assert len(books) > 0
    assert books[0]["author"] == "Test Author"
