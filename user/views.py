from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions

from user.serializers import (
    UserListSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    list_serializer_class = UserListSerializer
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

    def list(self, request, *args, **kwargs):
        self.serializer_class = self.list_serializer_class
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = self.list_serializer_class
        self.permission_classes = (permissions.AllowAny,)
        return super().create(request, *args, **kwargs)
