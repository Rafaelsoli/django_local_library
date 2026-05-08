# ─── Schemas ──────────────────────────────────────────────────────────────────
from datetime import date
from typing import Optional
import uuid
from ninja import Schema
    
class GenreSchema(Schema):
    id: int
    name: str

class AuthorOut(Schema):
    id: int
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    date_of_death: Optional[date] = None

class AuthorIn(Schema):
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    date_of_death: Optional[date] = None

class BookOut(Schema):
    id: int
    title: str
    summary: str
    isbn: str
    author: Optional[AuthorOut] = None
    genre: list[GenreSchema] = []

class BookIn(Schema):
    title: str
    summary: str
    isbn: str
    author_id: int
    genre_ids: list[int]

class BookInstanceOut(Schema):
    id: uuid.UUID
    status: str
    imprint: str
    due_back: Optional[date] = None

    @staticmethod
    def resolve_book_title(obj):
        return obj.book.title

class RenewSchema(Schema):
    renewal_date: date

class StatsOut(Schema):
    books: int
    copies: int
    copies_available: int
    authors: int