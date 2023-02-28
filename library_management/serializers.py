from rest_framework import serializers

from library_management.models import Book, BookOrder, BookIssue, Genre, BookOrderDetail
from accounts.serializers import UserSerializer


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'isbn', 'title', 'author', 'date_written']


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


class GenreSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=True)

    class Meta:
        model = Genre
        fields = ['id', 'title', 'book']


class BookIssueSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = BookIssue
        read_only_fields = ['status']

    fields = ['id', 'book', 'user', 'status', 'date']
