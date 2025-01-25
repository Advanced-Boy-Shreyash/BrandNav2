from fastapi import HTTPException


def borrow_book(connection, record):
    try:
        cursor = connection.cursor()

        # Check if the book is already borrowed
        cursor.execute(
            "SELECT is_returned FROM borrow_records WHERE book_id = ? AND is_returned = 0",
            (record.book_id,),
        )
        if cursor.fetchone():
            return {"message": "Book is already borrowed"}

        # Insert a new borrow record
        cursor.execute(
            "INSERT INTO borrow_records (book_id, user_id, borrow_date, is_returned) VALUES (?, ?, ?, 0)",
            (record.book_id, record.user_id, record.borrow_date),
        )
        connection.commit()
        return {"message": "Book borrowed successfully"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error borrowing book: {e}")
    finally:
        connection.close()


def return_book(connection, record_id):
    try:
        cursor = connection.cursor()

        # Check if the book has already been returned
        cursor.execute(
            "SELECT is_returned FROM borrow_records WHERE id = ?",
            (record_id,),
        )
        borrow_record = cursor.fetchone()
        if not borrow_record:
            return {"message": "Borrow record not found"}
        if borrow_record['is_returned'] == 1:
            return {"message": "Book has already been returned"}

        # Mark the book as returned
        cursor.execute(
            "UPDATE borrow_records SET is_returned = 1, return_date = CURRENT_DATE WHERE id = ?",
            (record_id,),
        )
        connection.commit()
        return {"message": "Book returned successfully"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error returning book: {e}")
    finally:
        connection.close()
