import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app)

@pytest.fixture
def add_sample_data():
    # Add sample data for books and users
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "genre": "Fiction",
        "publication_year": 2021
    }
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone_number": "1234567890"
    }
    # Add Book
    response = client.post("/books/", json=book_data)
    book_id = response.json()['id']
    
    # Add User
    response = client.post("/users/", json=user_data)
    user_id = response.json()['id']
    
    return book_id, user_id

def test_borrow_book(add_sample_data):
    book_id, user_id = add_sample_data
    borrow_record = {
        "book_id": book_id,
        "user_id": user_id,
        "borrow_date": str(datetime.now())
    }
    response = client.post("/borrow/", json=borrow_record)
    assert response.status_code == 200
    assert response.json() == {"message": "Book borrowed successfully"}

def test_borrow_book_already_borrowed(add_sample_data):
    book_id, user_id = add_sample_data
    borrow_record = {
        "book_id": book_id,
        "user_id": user_id,
        "borrow_date": str(datetime.now())
    }
    client.post("/borrow/", json=borrow_record)  # First borrow
    response = client.post("/borrow/", json=borrow_record)  # Try borrowing again
    assert response.status_code == 400
    assert response.json() == {"detail": "Book is already borrowed"}

def test_return_book(add_sample_data):
    book_id, user_id = add_sample_data
    borrow_record = {
        "book_id": book_id,
        "user_id": user_id,
        "borrow_date": str(datetime.now())
    }
    # Borrow the book
    response = client.post("/borrow/", json=borrow_record)
    record_id = response.json()['record_id']
    
    # Return the book
    response = client.post(f"/borrow/return/{record_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Book returned successfully"}

def test_return_non_existing_book():
    # Try returning a non-existing borrow record
    response = client.post("/borrow/return/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Borrow record not found"}