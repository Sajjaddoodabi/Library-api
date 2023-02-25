from rest_framework import serializers

from accounts.models import User, Librarian


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('is_librarian', 'is_active')
        fields = ['id', 'username', 'email', 'password', 'is_librarian', 'is_active']


class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarian
        read_only_fields = ('is_librarian', 'is_active')
        fields = ['id', 'username', 'email', 'card_number', 'is_librarian', 'is_active']
