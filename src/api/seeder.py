import sys
sys.path.append('../')
from api.authors import sync_books_and_author
from api.database import SessionLocal
import json
import models

db = SessionLocal()
seed_file = open('seed.json')
authors = json.load(seed_file)

for author in authors:
    author_exists = db.query(models.Author).filter(models.Author.name == author['name']).first()
    if author_exists is not None:
        print(f"Author {author['name']} already exists!")
        continue
    author_data = author
    books = author_data.pop("books", [])
    db_author = models.Author(**author_data)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    sync_books_and_author(author_id=db_author.id, books=books, db=db)

db.close()

print("Seed complete!")