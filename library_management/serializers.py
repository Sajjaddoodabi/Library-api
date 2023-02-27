from rest_framework import serializers

from library_management.models import Book, BookOrder, BookIssue, Genre
from accounts.serializers import UserSerializer


class BookSerializer(serializers.ModelSerializer):
    model = Book
    fields = ['id', 'isbn', 'title', 'author', 'date_written']


class BookOrderSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    model = BookOrder
    fields = ['id', 'book', 'user', 'date_taken']


class GenreSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=True)

    model = Genre
    fields = ['id', 'title', 'book']


class BookIssueSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    model = BookIssue
    read_only_field = ['status']
    fields = ['id', 'book', 'user', 'status', 'date']
