from rest_framework.permissions import BasePermission
from users.models import UserRoles


class IsOwner(BasePermission):
    message = 'Доступ запрещен. Вы не являетесь владельцем.'

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsModerator(BasePermission):
    message = 'Доступ запрещен. Вы не являетесь модератором'

    def has_permission(self, request, view):
        if request.user.role == UserRoles.MODERATOR:
            return True
        return False
