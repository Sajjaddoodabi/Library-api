from django.urls import path
from .views import UserRegisterView, LibrarianRegisterView, LoginView, LogoutView, UserView, ChangePasswordView

urlpatterns = [
    path('register/user/', UserRegisterView.as_view()),
    path('register/librarian/', LibrarianRegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user/', UserView.as_view()),
    path('user/change-password/', ChangePasswordView.as_view()),
]
