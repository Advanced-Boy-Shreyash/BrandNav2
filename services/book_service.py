from fastapi import HTTPException


def add_book_to_db(connection, book):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, genre, publication_year) VALUES (?, ?, ?, ?)",
            (book.title, book.author, book.genre, book.publication_year),
        )
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error adding book to database: {e}")
    finally:
        connection.close()


def get_books_from_db(connection, author=None, genre=None):
    try:
        cursor = connection.cursor()
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
        cursor.execute(query, params)
        books = cursor.fetchall()

        if not books:
            raise HTTPException(
                status_code=404, detail="No books found matching the criteria")

        return books
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving books: {e}")
    finally:
        connection.close()
