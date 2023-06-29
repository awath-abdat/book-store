from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import Field
import models

# Authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode=True

class UserToken(UserBase):
    password: str

# Books
class BookAuthor(BaseModel):
    id: Optional[int]
    name: str

    class Config:
        orm_mode=True

class Book(BaseModel):
    author_id: int
    name: str
    number_of_pages: int

    class Config:
        orm_mode=True

class BookResponse(BaseModel):
    id: Optional[int]
    author_id: int
    name: str
    number_of_pages: int

    author: BookAuthor

    class Config:
        orm_mode=True

# Authors
class AuthorBook(BaseModel):
    name: str
    number_of_pages: int

    class Config:
        orm_mode=True

class AuthorResponse(BaseModel):
    id: Optional[int]
    name: str
    books: List[Book] = []

    class Config:
        orm_mode=True

class AuthorRequest(BaseModel):
    name: str
    books: List[AuthorBook] = []

    class Config:
        orm_mode=True