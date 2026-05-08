from ninja import NinjaAPI, Schema
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from django.http import HttpError
from catalog.models import Book, Author, BookInstance, Genre
from datetime import date
from uuid import UUID
from typing import Optional
from .schemas.Schemas import *
api = NinjaAPI()

# ─── Books ────────────────────────────────────────────────────────────────────

@api.get("/books", response=list[BookOut])
def list_books(request):
    return Book.objects.select_related("author").prefetch_related("genre").all()

@api.get("/books/{book_id}", response=BookOut)
def get_book(request, book_id: int):
    return get_object_or_404(Book, pk=book_id)

@api.post("/books", response=BookOut, auth=django_auth)
def create_book(request, payload: BookIn):
    book = Book.objects.create(
        title=payload.title,
        summary=payload.summary,
        isbn=payload.isbn,
        author_id=payload.author_id,
    )
    book.genre.set(payload.genre_ids)
    return book

@api.put("/books/{book_id}", response=BookOut, auth=django_auth)
def update_book(request, book_id: int, payload: BookIn):
    book = get_object_or_404(Book, pk=book_id)
    for attr, value in payload.dict(exclude={"genre_ids"}).items():
        setattr(book, attr, value)
    book.genre.set(payload.genre_ids)
    book.save()
    return book

@api.delete("/books/{book_id}", auth=django_auth)
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return {"success": True}


# ─── Authors ──────────────────────────────────────────────────────────────────

@api.get("/authors", response=list[AuthorOut])
def list_authors(request):
    return Author.objects.all()

@api.get("/authors/{author_id}", response=AuthorOut)
def get_author(request, author_id: int):
    return get_object_or_404(Author, pk=author_id)

@api.post("/authors", response=AuthorOut, auth=django_auth)
def create_author(request, payload: AuthorIn):
    return Author.objects.create(**payload.dict())

@api.put("/authors/{author_id}", response=AuthorOut, auth=django_auth)
def update_author(request, author_id: int, payload: AuthorIn):
    author = get_object_or_404(Author, pk=author_id)
    for attr, value in payload.dict().items():
        setattr(author, attr, value)
    author.save()
    return author

@api.delete("/authors/{author_id}", auth=django_auth)
def delete_author(request, author_id: int):
    author = get_object_or_404(Author, pk=author_id)
    author.delete()
    return {"success": True}


# ─── Loans ────────────────────────────────────────────────────────────────────

@api.get("/loans/mine", response=list[BookInstanceOut], auth=django_auth)
def my_loans(request):
    return BookInstance.objects.filter(
        borrower=request.user, status="o"
    ).select_related("book")

@api.get("/loans/all", response=list[BookInstanceOut], auth=django_auth)
def all_loans(request):
    if not request.user.has_perm("catalog.can_mark_returned"):
        raise HttpError(403, "Sem permissão")
    return BookInstance.objects.filter(status="o").select_related("book")

@api.post("/loans/{instance_id}/renew", auth=django_auth)
def renew_loan(request, instance_id: UUID, payload: RenewSchema):
    instance = get_object_or_404(BookInstance, pk=instance_id)
    if instance.borrower != request.user and not request.user.has_perm("catalog.can_mark_returned"):
        raise HttpError(403, "Sem permissão")
    instance.due_back = payload.renewal_date
    instance.save()
    return {"success": True}

# catalog/api.py

@api.get("/stats", response=StatsOut)
def get_stats(request):
    return {
        "books":            Book.objects.count(),
        "copies":           BookInstance.objects.count(),
        "copies_available": BookInstance.objects.filter(status="a").count(),
        "authors":          Author.objects.count(),
    }