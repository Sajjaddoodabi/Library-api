import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

from accounts.permissions import IsAdmin, IsAdminOrReadOnly, IsLibrarian, IsAuthenticated
from accounts.views import get_user
from library_management.models import Book, BookOrder, Genre, BookIssue, BookOrderDetail
from library_management.serializers import BookSerializer, BookOrderDetailSerializer, GenreSerializer, \
    BookIssueSerializer, BookOrderSerializer, BookIssueMiniSerializer


class CreateBookView(APIView):
    # permission_classes = (IsLibrarian,)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            isbn = serializer.data['isbn']
            title = serializer.data['title']
            author = serializer.data['author']
            date_written = serializer.data['date_written']
            genre = request.data['genre']

            genre = Genre.objects.filter(title=genre).first()
            if not genre:
                response = {'detail': 'genre NOT found!'}
                return Response(response)

            try:
                book = Book.objects.create(isbn=isbn, title=title, author=author, date_written=date_written)
            except Exception as e:
                return Response(str(e))

            genre = Genre.objects.create(title=genre, book_id=book.id)

            book_ser = BookSerializer(book)
            return Response(book_ser.data)

        return Response(serializer.errors)


class BookDetailView(RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsLibrarian,)
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListView(ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CreateBookOrderDetailView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = BookOrderDetailSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user(request)
            book_id = request.data['book']
            book = Book.objects.filter(id=book_id).first()

            if not user:
                response = {'detail': 'user NOT found!'}
                return Response(response)

            if not book:
                response = {'detail': 'book NOT found!'}
                return Response(response)

            order, created = BookOrder.objects.get_or_create(user_id=user.id, status='open')

            book_exist = BookOrderDetail.objects.filter(order=order, book_id=book_id).exists()
            if not book_exist:
                response = {'detail': 'you already have tis book in your order!'}
                return Response(response)

            BookOrderDetail.objects.create(order=order, book_id=book.id)

            date_return = order.date_taken + datetime.timedelta(days=15)
            order.date_return = date_return
            order.save()

            order_ser = BookOrderSerializer(order)
            return Response(order_ser.data)

        return Response(serializer.errors)


class BookOrderDetailView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = get_user(request)
        order = BookOrderDetail.objects.filter(pk=pk).first()

        if user == order.order.user:
            serializer = BookOrderDetailSerializer(order)
            return Response(serializer.data)

        response = {'detail': 'Not found!'}
        return Response(response)

    # def put(self, request, pk):
    #     serializer = BookOrderDetailSerializer(data=request.data)
    #     if serializer.is_valid():
    #         pass
    #     return Response(serializer.errors)

    def delete(self, request, pk):
        user = get_user(request)
        order = BookOrderDetail.objects.filter(pk=pk).first()

        if user == order.order.user:
            order.delete()

            response = {'detail': f'book order with id {order.id} deleted successfully!'}
            return Response(response)

        response = {'detail': 'Not found!'}
        return Response(response)



class BookOrderConfirm(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = get_user(request)
        order = BookOrder.objects.filter(user_id=user.id, status='open').first()
        order_detail = BookOrderDetail.objects.filter(order=order)

        if not order:
            response = {'detail': 'order NOT found!'}
            return Response(response)

        for detail in order_detail:
            detail.book.available = False
            detail.book.save()

        if order.status == 'progress':
            order.status = 'done'
            order.save()

        response = {'detail': 'confirmed!'}
        return Response(response)


class BookOrderCancel(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = get_user(request)
        order = BookOrder.objects.filter(user_id=user.id, status='open').first()

        if not order:
            response = {'detail': 'order NOT found!'}
            return Response(response)

        order.status = 'cancelled'

        response = {'detail': 'cancelled!'}
        return Response(response)


class BookOrderView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = get_user(request)
        order = BookOrder.objects.filter(pk=pk).first()

        if user == order.user:
            serializer = BookOrderSerializer(order)
            return Response(serializer.data)

        response = {'detail': 'Not found!'}
        return Response(response)

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        user = get_user(request)
        order = BookOrder.objects.filter(pk=pk).first()

        if user == order.user:
            order.delete()

            response = {'detail': f'book order with id {order.id} deleted successfully!'}
            return Response(response)

        response = {'detail': 'Not found!'}
        return Response(response)

class ChangeOrderDateReturn(APIView):
    # permission_classes = (IsLibrarian,)

    def patch(self, request, pk):
        order = BookOrder.objects.filter(pk=pk).first()
        date_return = request.data['date_return']

        if not order:
            response = {'detail': 'order NOT found!'}
            return Response(response)

        if not date_return:
            response = {'detail': 'field required!'}
            return Response(response)

        order.date_return = date_return
        order.save()

        order_ser = BookOrderSerializer(order)
        return Response(order_ser.data)


class ChangeOrderProgress(APIView):
    # permission_classes = (IsLibrarian,)

    def patch(self, request, pk):
        order = BookOrder.objects.filter(pk=pk).first()

        if not order:
            response = {'detail': 'issue NOT found!'}
            return Response(response)

        if order.status == 'requested':
            order.status = 'progress'
            order.save()

            response = {'detail': 'order status changed to progress!'}
            return Response(response)

        response = {'detail': 'cant change this status!'}
        return Response(response)


class BookOrderListView(ListAPIView):
    # permission_classes = (IsAdmin,)
    queryset = BookOrder.objects.all()
    serializer_class = BookOrderSerializer


class CreateGenreView(APIView):
    # permission_classes = (IsAdmin,)

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.data['title']

            genre = Genre.objects.create(title=title)
            genre_ser = GenreSerializer(genre)

            return Response(genre_ser.data)
        return Response(serializer.errors)


class GenreDetailView(RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAdmin,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreListView(ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CreateBookIssueView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        serializer = BookIssueSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user(request)
            book = Book.objects.filter(pk=pk).first()
            description = serializer.data['description']

            if not user:
                response = {'detail': 'user NOT found!'}
                return Response(response)

            if not book:
                response = {'detail': 'book NOT found!'}
                return Response(response)

            issue = BookIssue.objects.create(user=user, book=book, description=description)
            issue_ser = BookIssueSerializer(issue)

            return Response(issue_ser.data)
        return Response(serializer.errors)


class BookIssueDetailView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = get_user(request)
        book_issue = BookIssue.objects.filter(pk=pk).first()

        if user == book_issue.user:
            serializer = BookIssueSerializer(book_issue)
            return Response(serializer.data)

        response = {'detail': 'Not found!'}
        return Response(response)

    def patch(self, request, pk):
        serializer = BookIssueSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user(request)
            book = Book.objects.filter(pk=pk).first()
            description = serializer.data['description']

            if not user:
                response = {'detail': 'user NOT found!'}
                return Response(response)

            if not book:
                response = {'detail': 'book NOT found!'}
                return Response(response)

            issue = BookIssue.objects.filter(user=user, book=book, description=description).first()
            if not issue:
                response = {'detail': 'issue NOT found!'}
                return Response(response)

            issue.description = description
            issue.save()

            issue_ser = BookIssueSerializer(issue)

            return Response(issue_ser.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        user = get_user(request)
        book_issue = BookIssue.objects.filter(pk=pk).first()

        if user == book_issue.user:
            book_issue.delete()

            response = {'detail': f'book issue with id {book_issue.id} deleted successfully!'}
            return Response(response)

        response = {'detail': 'Not found!'}
        return Response(response)


class BookIssueListView(ListAPIView):
    # permission_classes = (IsAdmin,)
    queryset = BookIssue
    serializer_class = BookIssueSerializer


class ChangeIssueProgress(APIView):
    # permission_classes = (IsAdmin,)

    def patch(self, request, pk):
        issue = BookIssue.objects.filter(pk=pk).first()

        if not issue:
            response = {'detail': 'issue NOT found!'}
            return Response(response)

        if issue.status == 'requested':
            issue.status = 'progress'
            issue.save()

            response = {'detail': 'issue status changed to progress!'}
            return Response(response)

        response = {'detail': 'cant change this status!'}
        return Response(response)


class ChangeIssueStatus(APIView):
    # permission_classes = (IsAdmin,)

    def patch(self, request, pk):
        serializer = BookIssueMiniSerializer(data=request.data)
        if serializer.is_valid():
            issue = BookIssue.objects.filter(pk=pk).first()
            status = serializer.data['status']

            if not issue:
                response = {'detail': 'issue NOT found!'}
                return Response(response)

            if issue.status == 'requested':
                issue.status = status
                issue.save()

                response = {'detail': f'issue status changed to {status}!'}
                return Response(response)

            response = {'detail': 'cant change this status!'}
            return Response(response)
        return Response(serializer.errors)
