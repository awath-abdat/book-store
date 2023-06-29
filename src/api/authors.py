

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.auth import get_current_active_user
from api.database import get_db

from api.schemas import AuthorResponse, AuthorRequest, AuthorBook, UserBase
import models

author_router = APIRouter()

def sync_books_and_author(author_id: int, books: AuthorBook, db: Session):
    book_names = [book['name'] for book in books]
    db.query(models.Book).filter(models.Book.author_id == author_id, models.Book.name.not_in(book_names)).delete()
    author_books = db.query(models.Book).filter(models.Book.author_id == author_id, models.Book.name.in_(book_names)).all()
    author_books_names = [book.name for book in author_books]
    new_books = [book for book in books if not book['name'] in author_books_names]
    for book in new_books:
        book['author_id'] = author_id
    new_books_db = [models.Book(**book) for book in new_books]
    db.bulk_save_objects(new_books_db)
    db.commit()


@author_router.post("/authors", response_model=AuthorResponse)
async def create_author(current_user: Annotated[UserBase, Depends(get_current_active_user)], author: AuthorRequest, db: Session = Depends(get_db)):
    author_exists = db.query(models.Author).filter(models.Author.name == author.name).first()
    if author_exists is not None:
        raise HTTPException(status_code=400, detail="Author already exists!")
    author_data = author.dict()
    books = author_data.pop("books", [])
    db_author = models.Author(**author_data)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    sync_books_and_author(author_id=db_author.id, books=books, db=db)
    return db_author

@author_router.get("/authors", response_model=list[AuthorResponse])
def read_authors(current_user: Annotated[UserBase, Depends(get_current_active_user)], skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    authors = db.query(models.Author).offset(skip).limit(limit).all()
    return authors

@author_router.get("/authors/{author_id}", response_model=AuthorResponse)
def read_author(current_user: Annotated[UserBase, Depends(get_current_active_user)], author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@author_router.patch("/authors/{author_id}", response_model=AuthorResponse)
def edit_author(current_user: Annotated[UserBase, Depends(get_current_active_user)], author_id: int, author: AuthorRequest, db: Session = Depends(get_db)):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    author_data = author.dict(exclude_unset=True, exclude_none=True)
    books = author_data.pop("books", [])
    for key, value in author_data.items():
        setattr(db_author, key, value)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    sync_books_and_author(author_id=db_author.id, books=books, db=db)
    return db_author