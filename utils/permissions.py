from rest_framework import permissions


class OnlyCreationWithoutAuth(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if view.action in ('option', 'create'):
            return True

        return super().has_permission(request, view)
