from django.urls import (
    include,
    path,
)

from user.routes import user_router


urlpatterns = [
    path('user/', include(user_router.urls)),
]
