from rest_framework import serializers

from accounts.models import User, Librarian


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('is_librarian', 'is_active')
        fields = ['id', 'username', 'email', 'password', 'is_librarian', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('is_librarian', 'is_active')
        fields = ['id', 'username', 'email', 'mobile', 'is_librarian', 'is_active']
        extra_kwargs = {
            'mobile': {'required': False}
        }


class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarian
        read_only_fields = ('is_librarian', 'is_active')
        fields = ['id', 'username', 'email', 'card_number', 'mobile', 'is_librarian', 'is_active']
        extra_kwargs = {
            'mobile': {'required': False}
        }


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    model = User
    read_only_fields = ('is_librarian', 'is_active')
    fields = ['current_password', 'new_password', 'confirm_password']
