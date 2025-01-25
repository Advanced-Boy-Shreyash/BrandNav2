from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: Optional[int]
    title: str
    author: str
    genre: str
    publication_year: int

class User(BaseModel):
    id: Optional[int]
    name: str
    email: str
    phone_number: str

class BorrowRecord(BaseModel):
    id: Optional[int]
    book_id: int
    user_id: int
    borrow_date: str
    return_date: Optional[str]
    is_returned: bool