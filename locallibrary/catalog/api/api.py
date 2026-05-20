from ninja import NinjaAPI, Schema
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from catalog.models import Book, Author, BookInstance, Genre
from datetime import date, timedelta
from uuid import UUID
from typing import Optional
from .schemas.Schemas import *
from django.contrib.auth import authenticate, login, logout
api = NinjaAPI()
# mudarpratruedepois

# ─── Logsin ────────────────────────────────────────────────────────────────────

@api.post("/login")
def login_user(request, data: LoginSchema):
    user = authenticate(request, username=data.username, password=data.password)
    if user is not None:
        login(request, user)
        return {"success": True, "username": user.username,}
    return api.create_response(request, {"error": "Invalid credentials"}, status=401)

@api.post("/logout")
def logout_user(request):
    logout(request)
    return {"success": True}

@api.get("/me")
def get_me(request):
    if request.user.is_authenticated:
        return {"username": request.user.username, "authenticated": True, "is_admin": request.user.is_staff}
    return {"authenticated": False}

# ─── lrivo ────────────────────────────────────────────────────────────────────

@api.get("/genres", response=list[GenreOut])
def list_genres(request):
    return Genre.objects.all()

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
    genres = Genre.objects.filter(name__in=payload.genre_ids)
    book.genre.set(genres)
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
    if book.bookinstance_set.filter(status = "o").exists():
        raise HttpError(400, "Não é possível deletar um livro que tem cópias emprestadas")
    else:
        book.delete()
    return {"success": True}


# ─── Aurotes ──────────────────────────────────────────────────────────────────

@api.get("/authors", response=list[AuthorOut])
def list_authors(request):
    return Author.objects.all()

@api.get("/authors/{author_id}", response=AuthorOutMinimo)
def get_author(request, author_id: int):
    author = get_object_or_404(Author.objects.prefetch_related("book_set"), pk=author_id)
    return author

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
    if author.book_set.exists():
        raise HttpError(400, "Não é possível deletar um autor que tem livros associados")
    else:
        author.delete()
    return {"success": True}


# ─── Alumagentos ────────────────────────────────────────────────────────────────────

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
def renew_loan(request, instance_id: UUID):
    instance = get_object_or_404(BookInstance, pk=instance_id)
    if instance.borrower != request.user and not request.user.has_perm("catalog.can_mark_returned"):
        raise HttpError(403, "Sem permissão")
    instance.due_back = date.today() + timedelta(days = 7)
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