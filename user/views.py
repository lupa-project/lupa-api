from django.contrib.auth.models import User
from rest_framework import viewsets

from user.serializers import UserSerializer
from utils.permissions import OnlyCreationWithoutAuth


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (OnlyCreationWithoutAuth,)
