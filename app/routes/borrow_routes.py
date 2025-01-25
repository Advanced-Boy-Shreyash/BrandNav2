from fastapi import APIRouter, HTTPException
from database import get_db_connection
from database.models import BorrowRecord
from datetime import datetime

router = APIRouter()


@router.post("/")
def borrow_book(record: BorrowRecord):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the book exists
    cursor.execute("SELECT * FROM books WHERE id = ?", (record.book_id,))
    book = cursor.fetchone()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if the user exists
    cursor.execute("SELECT * FROM users WHERE id = ?", (record.user_id,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the book is already borrowed
    cursor.execute("SELECT is_returned FROM borrow_records WHERE book_id = ? AND is_returned = 0",
                   (record.book_id,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Book is already borrowed")

    # Validate the date format
    try:
        borrow_date = datetime.strptime(record.borrow_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Insert the borrow record
    cursor.execute("INSERT INTO borrow_records (book_id, user_id, borrow_date, is_returned) VALUES (?, ?, ?, 0)",
                   (record.book_id, record.user_id, borrow_date))
    conn.commit()
    conn.close()

    return {"message": "Book borrowed successfully"}


@router.put("/return/{record_id}")
def return_book(record_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE borrow_records SET is_returned = 1, return_date = CURRENT_DATE WHERE id = ?",
                   (record_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    conn.close()
    return {"message": "Book returned successfully"}
