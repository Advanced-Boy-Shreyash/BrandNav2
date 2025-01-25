from fastapi import HTTPException


def add_user_to_db(connection, user):
    try:
        cursor = connection.cursor()

        # Check if the user already exists (by email)
        cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
        if cursor.fetchone():
            return {"message": "User with this email already exists."}

        # Insert the new user
        cursor.execute(
            "INSERT INTO users (name, email, phone_number) VALUES (?, ?, ?)",
            (user.name, user.email, user.phone_number),
        )
        connection.commit()
        return {"message": "User added successfully", "user_id": cursor.lastrowid}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding user: {e}")
    finally:
        connection.close()


def get_users_from_db(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return users if users else {"message": "No users found."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching users: {e}")
    finally:
        connection.close()
