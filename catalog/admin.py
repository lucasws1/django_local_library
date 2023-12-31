from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Register your models here.
admin.site.register(Genre)
admin.site.register(Language)


class BookInLine(admin.TabularInline):
    model = Book
    extra = 0


# Define the admin class
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "date_of_birth", "date_of_death")
    fields = ["first_name", "last_name", ("date_of_birth", "date_of_death")]
    inlines = [BookInLine]


class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    extra = 0


# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_genre")
    inlines = [BookInstanceInLine]


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book", "status", "borrower", "due_back", "id")
    list_filter = ("status", "due_back")

    fieldsets = (
        (None, {"fields": ("book", "imprint", "id")}),
        ("Availability", {"fields": ("status", "due_back", "borrower")}),
    )
