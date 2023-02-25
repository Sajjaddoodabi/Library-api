from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('is_librarian', 'is_active')
        fields = ['id', 'username', 'email', 'password', 'is_librarian', 'is_active']
