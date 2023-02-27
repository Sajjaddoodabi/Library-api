import jwt
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from accounts.models import User


def get_user(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user = User.objects.filter(id=payload['id']).first()

    return user


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
