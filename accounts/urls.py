from django.urls import path
from .views import UserRegisterView

urlpatterns = [
    path('register/user/', UserRegisterView.as_view()),
]
