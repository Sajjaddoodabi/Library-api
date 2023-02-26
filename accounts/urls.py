from django.urls import path
from .views import UserRegisterView, LibrarianRegisterView, LoginView, LogoutView

urlpatterns = [
    path('register/user/', UserRegisterView.as_view()),
    path('register/librarian/', LibrarianRegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]
