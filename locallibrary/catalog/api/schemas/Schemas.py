# ─── Schemas ──────────────────────────────────────────────────────────────────
from datetime import date
from typing import Optional
import uuid
from ninja import Field, Schema

class LoginSchema(Schema):
    username: str
    password: str


class GenreSchema(Schema):
    id: int
    name: str
class BookInstanceSchema(Schema):
    id: uuid.UUID
    imprint: str
    status: str
    due_back: Optional[date] = None

class AuthorIn(Schema):
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    date_of_death: Optional[date] = None

class BookOutMinimo(Schema):
    id: int
    title: str
    summary: str
    
class AuthorOutMinimo(Schema):
    id: int
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    date_of_death: Optional[date] = None
    books: list[BookOutMinimo] = Field(..., alias="book_set")

class AuthorOut(Schema):
    id: int
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    date_of_death: Optional[date] = None

class GenreOut(Schema):
    name: str

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
    genre_ids: list[str]

class BookInstanceOut(Schema):
    id: uuid.UUID
    status: str
    imprint: str
    due_back: Optional[date] = None
    titulo_livro: Optional[str] = Field("Sem título", alias="book.title")

    def resolve_titulo_livro(self, obj):
        if obj.book and hasattr(obj.book, 'title'):
            return obj.book.title
        return "Livro não associado"

class RenewSchema(Schema):
    renewal_date: date

class StatsOut(Schema):
    books: int
    copies: int
    copies_available: int
    authors: int