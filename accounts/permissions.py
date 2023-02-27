from rest_framework.permissions import SAFE_METHODS, BasePermission
from .views import get_user


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user = get_user(request)
        if request.method in SAFE_METHODS:
            return True
        return bool(user and user.is_authenticated)


class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user = get_user(request)
        if request.method in SAFE_METHODS:
            return True
        return user.is_anonymous


class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        user = get_user(request)
        if request.method in SAFE_METHODS:
            return True
        return bool(user.is_authenticated and user.is_librarian)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = get_user(request)
        if request.method in SAFE_METHODS:
            return True
        return bool(user and user.is_staff)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = get_user(request)
        if request.method in SAFE_METHODS:
            return True
        return bool(user and user.is_staff)
