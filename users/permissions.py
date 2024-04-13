from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = 'Доступ запрещен. Вы не являетесь владельцем.'

    def has_object_permission(self, request, view, obj):
        return obj == request.user
