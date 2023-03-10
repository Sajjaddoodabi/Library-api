from django.urls import path
from .views import CreateBookView, BookDetailView, BookListView, BookOrderDetailView, \
    CreateGenreView, GenreDetailView, GenreListView, CreateBookIssueView, \
    BookIssueDetailView, BookIssueListView, BookOrderListView, CreateBookOrderDetailView, BookOrderView, \
    BookOrderConfirm, BookOrderCancel, ChangeIssueStatus, ChangeIssueProgress, ChangeOrderProgress, \
    ChangeOrderDateReturn, SearchBook, SearchAuthor, SearchGenre, SearchByDate

urlpatterns = [
    path('book/add-book/', CreateBookView.as_view()),
    path('book/detail/<int:pk>/', BookDetailView.as_view()),
    path('book/detail/<int:pk>/issue/add_issue/', CreateBookIssueView.as_view()),
    path('book/list/', BookListView.as_view()),
    path('book/genre/add-genre/', CreateGenreView.as_view()),
    path('book/genre/detail/<int:pk>/', GenreDetailView.as_view()),
    path('book/genre/list/', GenreListView.as_view()),
    path('book/issue/detail/<int:pk>', BookIssueDetailView.as_view()),
    path('book/issue/detail/<int:pk>/status/progress/', ChangeIssueProgress.as_view()),
    path('book/issue/detail/<int:pk>/status/', ChangeIssueStatus.as_view()),
    path('book/issue/list/', BookIssueListView.as_view()),
    path('book-order/detail/<int:pk>/', BookOrderView.as_view()),
    path('book-order/detail/<int:pk>/change-date-return/', ChangeOrderDateReturn.as_view()),
    path('book-order/detail/<int:pk>/progress/', ChangeOrderProgress.as_view()),
    path('book-order/add-book/', BookOrderDetailView.as_view()),
    path('book-order/detail/add-detail/', CreateBookOrderDetailView.as_view()),
    path('book-order/list/', BookOrderListView.as_view()),
    path('book-order/confirm/', BookOrderConfirm.as_view()),
    path('book-order/cancel/', BookOrderCancel.as_view()),

    path('search/title/<str:ttile>/', SearchBook.as_view()),
    path('search/author/<str:author>/', SearchAuthor.as_view()),
    path('search/genre/<str:genre>/', SearchGenre.as_view()),
    path('search/date/<str:date>/<str:to_date>', SearchByDate.as_view()),
]
