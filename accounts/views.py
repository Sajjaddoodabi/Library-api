from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User, Librarian
from accounts.serializers import UserSerializer


class UserRegisterView(APIView):
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
