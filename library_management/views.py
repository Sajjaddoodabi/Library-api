import datetime

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

from accounts.views import get_user
from library_management.models import Book, BookOrder, Genre, BookIssue, BookOrderDetail
from library_management.serializers import BookSerializer, BookOrderDetailSerializer, GenreSerializer, \
    BookIssueSerializer, BookOrderSerializer


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


class CreateBookOrderDetailView(APIView):
    def post(self, request):
        serializer = BookOrderDetailSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user(request)
            book_id = request.data['book']

            if not user:
                response = {'detail': 'user NOT found!'}
                return Response(response)

            book = Book.objects.filter(id=book_id).first()
            if not book:
                response = {'detail': 'book NOT found!'}
                return Response(response)

            if not book.available:
                response = {'detail': 'book NOT available!'}
                return Response(response)

            order, created = BookOrder.objects.get_or_create(user_id=user.id, status='open')
            BookOrderDetail.objects.create(order=order, book_id=book.id)

            date_return = order.date_taken + datetime.timedelta(days=15)
            order.date_return = date_return
            order.save()

            book.available = False
            book.save()

            order_ser = BookOrderSerializer(order)
            return Response(order_ser.data)

        return Response(serializer.errors)


class BookOrderDetailView(APIView):
    def get(self, request, pk):
        order = BookOrderDetail.objects.filter(pk=pk).first()
        serializer = BookOrderDetailSerializer(order)

        return Response(serializer.data)

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        order = BookOrderDetail.objects.filter(pk=pk).first()
        order.delete()

        response = {'detail': f'book order with id {order.id} deleted successfully!'}
        return Response(response)


class BookOrderView(APIView):
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
