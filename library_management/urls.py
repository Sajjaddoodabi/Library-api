from django.urls import path
from .views import CreateBookView, BookDetailView, BookListView, CreateBookOrderView, BookOrderListView, \
    BookOrderDetailView, AddBookToOrderView, CreateGenreView, GenreDetailView, GenreListView, CreateBookIssueView, \
    BookIssueDetailView, BookIssueListView

urlpatterns = [
    path('book/add-book/', CreateBookView.as_view()),
    path('book/detail/<int:pk>/', BookDetailView.as_view()),
    path('book/list/', BookListView.as_view()),
    path('book/genre/add-genre/', CreateGenreView.as_view()),
    path('book/genre/detail/<int:pk>/', GenreDetailView.as_view()),
    path('book/genre/list/', GenreListView.as_view()),
    path('book/issue/add_issue/', CreateBookIssueView.as_view()),
    path('book/issue/detail/<int:pk>', BookIssueDetailView.as_view()),
    path('book/issue/list/', BookIssueListView.as_view()),
    path('book-order/add-order/', CreateBookOrderView.as_view()),
    path('book-order/add-order/add-book/', AddBookToOrderView.as_view()),
    path('book-order/detail/<int:pk>/', BookOrderDetailView.as_view()),
    path('book-order/list/', BookOrderListView.as_view()),
]
