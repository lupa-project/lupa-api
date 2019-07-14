from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from rest_framework import serializers


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
            'date_joined',
            'last_login',
        )


class UserListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
        )

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save(update_fields=['password'])

        return user

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)

        return value
