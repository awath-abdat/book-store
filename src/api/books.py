

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.auth import get_current_active_user
from api.database import get_db

from api.schemas import Book, BookResponse, UserBase
import models

book_router = APIRouter()

@book_router.post("/books", response_model=BookResponse)
async def create_book(current_user: Annotated[UserBase, Depends(get_current_active_user)], book: Book, db: Session = Depends(get_db)):
    book_exists = db.query(models.Book).filter(models.Book.name == book.name, models.Book.author_id == book.author_id).first()
    if book_exists is not None:
        raise HTTPException(status_code=400, detail="Book with author already exists!")
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@book_router.get("/books", response_model=list[BookResponse])
def read_books(current_user: Annotated[UserBase, Depends(get_current_active_user)], skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books

@book_router.get("/books/{book_id}", response_model=BookResponse)
def read_book(current_user: Annotated[UserBase, Depends(get_current_active_user)], book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@book_router.patch("/books/{book_id}", response_model=BookResponse)
def edit_book(current_user: Annotated[UserBase, Depends(get_current_active_user)], book_id: int, book: Book, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    book_data = book.dict(exclude_unset=True, exclude_none=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book