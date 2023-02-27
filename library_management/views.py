from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

from library_management.models import Book, BookOrder, Genre, BookIssue
from library_management.serializers import BookSerializer, BookOrderSerializer, GenreSerializer, BookIssueSerializer


class CreateBookView(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            isbn = serializer.data['isbn']
            title = serializer.data['title']
            author = serializer.data['author']
            date_written = serializer.data['date_written']

            try:
                book = Book.objects.create(isbn=isbn, title=title, author=author, date_written=date_written)
            except Exception as e:
                return Response(str(e))

            book_ser = BookSerializer(book)
            return Response(book_ser.data)

        return Response(serializer.errors)


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
        order = BookOrder.objects.filter(pk=pk).first()
        serializer = BookOrderSerializer(order)

        return Response(serializer.data)

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        order = BookOrder.objects.filter(pk=pk).first()
        order.delete()

        response = {'detail': f'book order with id {order.id} deleted successfully!'}
        return Response(response)


class BookOrderListView(ListAPIView):
    queryset = BookOrder.objects.all()
    serializer_class = BookOrderSerializer


class CreateGenreView(APIView):
    def post(self, request):
        pass


class GenreDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreListView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CreateBookIssueView(APIView):
    def post(self, request):
        pass


class BookIssueDetailView(APIView):
    def get(self, request, pk):
        book_issue = BookIssue.objects.filter(pk=pk).first()
        serializer = BookIssueSerializer(book_issue)

        return Response(serializer.data)

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        book_issue = BookIssue.objects.filter(pk=pk).first()
        book_issue.delete()

        response = {'detail': f'book issue with id {book_issue.id} deleted successfully!'}
        return Response(response)


class BookIssueListView(ListAPIView):
    queryset = BookIssue
    serializer_class = BookIssueSerializer
