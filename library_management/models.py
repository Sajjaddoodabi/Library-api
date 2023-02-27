from django.db import models

from accounts.models import User


class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=200, blank=False, null=False)
    author = models.CharField(max_length=200)
    date_written = models.DateField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class BookOrder(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='order')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    date_taken = models.DateTimeField(auto_now_add=True)
    date_return = models.DateField()

    def __str__(self):
        return f'{self.book.title} - {self.user} - {self.date_return}'


class Genre(models.Model):
    title = models.CharField(max_length=100)
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, related_name='genre', null=True, blank=True)

    def __str__(self):
        return self.title


class BookIssue(models.Model):
    class RequestStatus(models.TextChoices):
        Requested = 'REQ', 'requested'
        Denied = 'DEN', 'denied'
        Done = 'DON', 'done'

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='book_issue')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_issue')
    status = models.CharField(max_length=20, choices=RequestStatus.choices, default=RequestStatus.Requested)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.book} - {self.status}'
