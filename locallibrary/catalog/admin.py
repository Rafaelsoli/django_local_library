from django.contrib import admin
from .models import Author, Genre, Book, BookInstance
# Register your models here.
#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)


class BooksInstanceInLine(admin.TabularInline):
    model = BookInstance

class BooksInLine(admin.TabularInline):
    model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display =('last_name', 'first_name', 'date_of_birth', 'date_of_death')
   

    fieldsets = (
        ('Name',{
            'fields': ('first_name', 'last_name')
        }),
        ('Birthdate',{
            'fields': ('date_of_birth', 'date_of_death')
        }),
    )

    inlines = [BooksInLine]


@admin.register(Book) 
class BookAdmin(admin.ModelAdmin):
    list_display=('title', 'author', 'display_genre')
    inlines = [BooksInstanceInLine]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        ('Information', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )