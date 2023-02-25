from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    address = models.CharField(max_length=300)
    is_librarian = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    @property
    def get_name(self):
        if self.first_name is None and self.last_name is None:
            return self.username
        else:
            return f'{self.first_name} {self.last_name}'


class Librarian(models.Model):
    parent_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='librarian')
    card_number = models.CharField(max_length=50)
    status = models.CharField(choices=[], max_length=100)

    def __str__(self):
        return self.parent_user.get_name
