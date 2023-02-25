from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_librarian = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    @property
    def get_name(self):
        if self.first_name is None and self.last_name is None:
            return self.username
        else:
            return f'{self.first_name} {self.last_name}'