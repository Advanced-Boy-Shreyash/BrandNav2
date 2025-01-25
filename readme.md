# Library Management System API

Here's a simple README template for your project:

Library Management System API
A backend API for managing books, users, and borrow records for a library management system built using FastAPI and SQLite.

## Features

- Books Management: Add, update, retrieve, and delete books.
- User Management: Add and retrieve users.
- Borrowing Books: Allows users to borrow and return books.

## Technologies

- FastAPI - Web framework for building APIs.
- SQLite - Lightweight database for storing books, users, and borrow records.
- Python 3.12 - Programming language used for the backend.

## Setup and Installation

### 1. Clone the repository

    git clone https://github.com/Advanced-Boy-Shreyash/BrandNav2
    cd BrandNav2

### 2. Run following commands

    pip install -r "requirements.txt"
    python run.py

# API Endpoints
## Books
- POST /books/ - Add a new book
- GET /books/ - Retrieve all books (filter by author and genre)
- PUT /books/{book_id} - Update book information
- DELETE /books/{book_id} - Delete a book

## Users
- POST /users/ - Add a new user
- GET /users/ - Retrieve all users

## Borrow Records
- POST /borrow/ - Borrow a book
- PUT /return/{record_id} - Return a borrowed book