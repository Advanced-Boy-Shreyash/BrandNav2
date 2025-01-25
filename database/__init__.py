import sqlite3

DATABASE_PATH = "library.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create books table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT NOT NULL,
        publication_year INTEGER NOT NULL
    )
    """)

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone_number TEXT NOT NULL
    )
    """)

    # Create borrow_records table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS borrow_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        user_id INTEGER,
        borrow_date TEXT NOT NULL,
        return_date TEXT,
        is_returned BOOLEAN NOT NULL,
        FOREIGN KEY (book_id) REFERENCES books (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    conn.commit()
    conn.close()


# Call create_tables when the application starts
create_tables()
