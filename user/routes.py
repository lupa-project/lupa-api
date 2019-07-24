from rest_framework.routers import DefaultRouter

from user.views import UserViewSet

user_router = DefaultRouter()

user_router.register(r'users', UserViewSet)
