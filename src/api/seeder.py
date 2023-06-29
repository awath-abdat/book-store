import sys
sys.path.append('../')
from api.authors import sync_books_and_author
from api.database import SessionLocal
from api.auth import get_password_hash
import json
import models

db = SessionLocal()

# Seed user
user_data = {"username": "abdat", "hashed_password": get_password_hash("DataCose@2023"), "is_active": True}
db_user = models.User(**user_data)
db.add(db_user)
db.commit()
db.refresh(db_user)
print("User with username 'abdat' and password 'DataCose@2023' seeded.")

# Seed authors and books
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