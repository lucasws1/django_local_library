from django.conf import settings
from datetime import date
from django.db import models
from django.urls import reverse  # Used to generate URLS by reversing the URL patterns
import uuid  # Required for unique book instances

# Create your models here.


class Genre(models.Model):
    # Model representing a book genre.
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)",
    )

    def __str__(self):
        # String for representing the Model object.
        return self.name

    def get_absolute_url(self):
        # Returns the url to access a particular genre instance.
        return reverse("genre-detail", args=[str(self.id)])


class Language(models.Model):
    name = models.CharField(
        max_length=200, unique=True, help_text="Enter the book's language"
    )

    def get_absolute_url(self):
        return reverse("language-detail", args=[str(self.id)])

    def __str__(self):
        return self.name


class Book(models.Model):
    # Model representing a book (but not a specific copy of a book).
    title = models.CharField(max_length=200)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author is a string rather than object because it hasn't been declared yet in file.
    author = models.ForeignKey("Author", on_delete=models.RESTRICT, null=True)
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book"
    )
    isbn = models.CharField(
        "ISBN", max_length=13, unique=True, help_text="13 character ISBN number"
    )
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.ForeignKey("Language", on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["title", "author"]

    def display_genre(self):
        # Creates a string for the genre. This is required to display genre in Admin.
        return ", ".join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = "Genre"

    def __str__(self):
        # String for representing the Model object.
        return self.title

    def get_absolute_url(self):
        # Returns the URL to access a detail record for this book.
        return reverse("book-detail", args=[str(self.id)])


class BookInstance(models.Model):
    # Model representing a specific copy of a book (i.e. that can be borrowed from the library)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this particular book across whole library",
    )
    book = models.ForeignKey("Book", on_delete=models.RESTRICT, null=True)
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    @property
    def is_overdue(self):
        # Determines if the book is overdue based on due date and current date.
        return bool(self.due_back and date.today() > self.due_back)

    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Book availability",
    )

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f"{self.id} ({self.book.title})"


class Author(models.Model):
    # Model representing an author.

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("died", null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
