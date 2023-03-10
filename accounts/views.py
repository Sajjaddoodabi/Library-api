import datetime

import jwt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from accounts.models import User, Librarian
from accounts.serializers import UserSerializer, ChangePasswordSerializer, LibrarianSerializer

from accounts.permissions import IsNotAuthenticated, IsAuthenticated, IsAdmin, IsAdminOrReadOnly, IsLibrarian


class UserRegisterView(APIView):
    permission_classes = (IsNotAuthenticated,)

    def post(self, request):
        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']

        except Exception as e:
            response = {'details': str(e)}
            return Response(response)

        try:
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()
        except Exception as e:
            response = {'details': str(e)}
            return Response(response)
        else:
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data)


class LibrarianRegisterView(APIView):
    permission_classes = (IsNotAuthenticated,)

    def post(self, request):
        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']

        except Exception as e:
            response = {'details': str(e)}
            return Response(response)

        try:
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)

            librarian = Librarian.objects.create(parent_user=user)
            librarian.parent_user.is_librarian = True

            librarian.save()
            user.save()

        except Exception as e:
            response = {'details': str(e)}
            return Response(response)
        else:
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data)


class LoginView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        if user is None:
            response = {'detail': 'User with Not found!'}
            return Response(response)

        if not user.check_password(password):
            response = {'detail': 'User with Not found!'}
            return Response(response)

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {'jwt': token}
        return response


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'detail': 'successfully logged out'}
        return response


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = get_user(request)
        if not user:
            response = {'detail': 'User NOT found!'}
            return Response(response)

        serializer = UserSerializer(user)
        return Response(serializer.data)


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


class UserLists(ListAPIView):
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LibrarianLists(ListAPIView):
    permission_classes = (IsAdmin,)
    queryset = User.objects.filter(is_librarian=True)
    serializer_class = LibrarianSerializer


class UserDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LibrarianDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsLibrarian,)
    queryset = User.objects.filter(is_librarian=True)
    serializer_class = LibrarianSerializer


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(request.data)
        if serializer.is_valid():
            current_password = serializer.data['current_password']
            new_password = serializer.data['new_password']
            confirm_password = serializer.data['confirm_password']

            user: User = get_user(request)

            if not user:
                raise AuthenticationFailed('User NOT found!')
            if user.check_password(current_password):
                raise AuthenticationFailed('User NOT found!')

            if new_password != confirm_password:
                response = {'detail': 'passwords do NOT match!'}
                return Response(response)

            user.set_password(confirm_password)
            ser = UserSerializer(user)
            user.save()

            return Response(ser.data)
        return Response(serializer.errors)
