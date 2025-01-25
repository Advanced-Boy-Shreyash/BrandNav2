from fastapi import APIRouter, HTTPException
from database import get_db_connection
from database.models import Book

router = APIRouter()


@router.post("/")
def add_book(book: Book):
    if not book.title or not book.author:
        raise HTTPException(status_code=400, detail="Title and author are required")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check for duplicate book by title and author
    cursor.execute("SELECT * FROM books WHERE title = ? AND author = ?", (book.title, book.author))
    existing_book = cursor.fetchone()
    if existing_book:
        raise HTTPException(status_code=400, detail="Book already exists")

    cursor.execute("INSERT INTO books (title, author, genre, publication_year) VALUES (?, ?, ?, ?)",
                   (book.title, book.author, book.genre, book.publication_year))
    conn.commit()
    conn.close()

    return {"message": "Book added successfully"}


@router.get("/")
def get_books(author: str = None, genre: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM books"
    params = []
    
    if author or genre:
        query += " WHERE"
        if author:
            query += " author = ?"
            params.append(author)
        if genre:
            query += (" AND" if author else "") + " genre = ?"
            params.append(genre)
    
    books = cursor.execute(query, params).fetchall()
    conn.close()

    if not books:
        raise HTTPException(status_code=404, detail="No books found matching the criteria")

    return books


@router.put("/{book_id}")
def update_book(book_id: int, book: Book):
    if not book.title or not book.author:
        raise HTTPException(status_code=400, detail="Title and author are required to update")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    existing_book = cursor.fetchone()

    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")

    cursor.execute("UPDATE books SET title = ?, author = ?, genre = ?, publication_year = ? WHERE id = ?",
                   (book.title, book.author, book.genre, book.publication_year, book_id))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="No changes made to the book")

    conn.close()
    return {"message": "Book updated successfully"}


@router.delete("/{book_id}")
def delete_book(book_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the book is being borrowed
    cursor.execute("SELECT * FROM borrow_records WHERE book_id = ? AND is_returned = 0", (book_id,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Cannot delete the book because it is currently borrowed")

    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    
    conn.close()
    return {"message": "Book deleted successfully"}