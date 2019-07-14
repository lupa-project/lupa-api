from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

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

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save(update_fields=['password'])

        return user

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)

        return value
