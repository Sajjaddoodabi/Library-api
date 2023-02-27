from django.urls import path
from .views import UserRegisterView, LibrarianRegisterView, LoginView, LogoutView, UserView, ChangePasswordView, \
    UserLists, LibrarianLists, UserDetail, LibrarianDetail

urlpatterns = [
    path('register/user/', UserRegisterView.as_view()),
    path('register/librarian/', LibrarianRegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user/', UserView.as_view()),
    path('user/detail/<int:pk>/', UserDetail.as_view()),
    path('user/detail/librarain/<int:pk>/', LibrarianDetail.as_view()),
    path('user/list/', UserLists.as_view()),
    path('user/list/librarain/', LibrarianLists.as_view()),
    path('user/change-password/', ChangePasswordView.as_view()),
]
