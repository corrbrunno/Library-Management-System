from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title
    
class Member(models.Model):
    member_id_validator = RegexValidator(
        regex=r'^\d{11}$',
        message='This field must contain exactly 11 digits.'
    )

    name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=11, validators=[member_id_validator])
    created_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.name}: {self.identifier}"


class BookLoan(models.Model):
    
    member = models.ForeignKey(Member,
                                on_delete=models.CASCADE,
                                unique=False
            )
    book = models.ForeignKey(Book, 
                                on_delete=models.PROTECT,
                                unique=False
            )
    books_borrowed = models.IntegerField()
    borrowed_date = models.DateTimeField(default=datetime.now)

    returned_date = models.DateTimeField(
        null=True, 
        blank=True 
    )
    
    @property
    def is_active(self):
        """Returns True if the book has not yet been returned."""
        return self.returned_date is None