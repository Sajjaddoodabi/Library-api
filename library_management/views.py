from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

from library_management.models import Book, BookOrder, Genre, BookIssue
from library_management.serializers import BookSerializer, BookOrderSerializer, GenreSerializer, BookIssueSerializer


class CreateBookView(APIView):
    def post(self, request):
        pass


class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CreateBookOrderView(APIView):
    def post(self, request):
        pass


class AddBookToOrderView(APIView):
    def post(self, request):
        pass


class BookOrderDetailView(APIView):
    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass


class BookOrderListView(ListAPIView):
    queryset = BookOrder.objects.all()
    serializer_class = BookOrderSerializer


class CreateGenreView(APIView):
    def post(self, request):
        pass


class GenreDetail(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreList(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CreateBookIssue(APIView):
    def post(self, request):
        pass


class BookIssueDetail(APIView):
    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass


class BookIssueList(ListAPIView):
    queryset = BookIssue
    serializer_class = BookIssueSerializer
