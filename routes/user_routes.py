from fastapi import APIRouter, HTTPException
from database import get_db_connection
from database.models import User

router = APIRouter()

@router.post("/")
def add_user(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users (name, email, phone_number) VALUES (?, ?, ?)",
                   (user.name, user.email, user.phone_number))
    conn.commit()
    conn.close()
    return {"message": "User added successfully"}

@router.get("/")
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    users = cursor.execute("SELECT * FROM users").fetchall()
    conn.close()
    return users

@router.put("/{user_id}")
def update_user(user_id: int, user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, email = ?, phone_number = ? WHERE id = ?",
                   (user.name, user.email, user.phone_number, user_id))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    conn.close()
    return {"message": "User updated successfully"}

@router.delete("/{user_id}")
def delete_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    conn.close()
    return {"message": "User deleted successfully"}