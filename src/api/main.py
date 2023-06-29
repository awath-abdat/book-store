import sys
from fastapi import FastAPI

sys.path.append('../')

from api.auth import auth_router
from api.authors import author_router
from api.books import book_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app = FastAPI()


app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Auth"],
)

app.include_router(
    author_router,
    prefix="/api",
    tags=["Authors"],
)

app.include_router(
    book_router,
    prefix="/api",
    tags=["Books"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
   expose_headers=["*"],
)