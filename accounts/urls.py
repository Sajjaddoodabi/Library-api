from django.urls import path
from .views import UserRegisterView, LibrarianRegisterView

urlpatterns = [
    path('register/user/', UserRegisterView.as_view()),
    path('register/librarian/', LibrarianRegisterView.as_view()),
]
