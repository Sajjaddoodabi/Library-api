from rest_framework import serializers

from library_management.models import Book, BookOrder, BookIssue, Genre, BookOrderDetail
from accounts.serializers import UserSerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'title']


class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Book
        fields = ['id', 'isbn', 'title', 'author', 'genre', 'date_written']


class BookOrderDetailSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source='book.title')

    class Meta:
        model = BookOrderDetail
        read_only_fields = ('order',)
        fields = ['id', 'order', 'book']


class BookOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    order_detail = BookOrderDetailSerializer(many=True)

    class Meta:
        model = BookOrder
        read_only_fields = ('status', 'date_return')
        fields = ['id', 'user', 'order_detail', 'date_taken', 'date_return', 'status']


class BookIssueSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = BookIssue
        read_only_fields = ['status']
        fields = ['id', 'book', 'user', 'description', 'status', 'date']


class BookIssueMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookIssue
        fields = ['status']