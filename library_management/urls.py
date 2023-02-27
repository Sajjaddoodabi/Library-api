from django.urls import path
from .views import CreateBookView, BookDetailView, BookListView, BookOrderDetailView, \
    CreateGenreView, GenreDetailView, GenreListView, CreateBookIssueView, \
    BookIssueDetailView, BookIssueListView, BookOrderListView, CreateBookOrderDetailView, BookOrderView

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
    path('book-order/detail/<int:pk>/', BookOrderView.as_view()),
    path('book-order/add-book/', BookOrderDetailView.as_view()),
    path('book-order/detail/add-detail/', CreateBookOrderDetailView.as_view()),
    path('book-order/list/', BookOrderListView.as_view()),
]
