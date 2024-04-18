from rest_framework.permissions import BasePermission
from users.models import UserRoles
from rest_framework.exceptions import PermissionDenied


class IsOwner(BasePermission):
    message = 'Доступ запрещен. Вы не являетесь владельцем'

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsModerator(BasePermission):
    message = 'Доступ запрещен. Вы не являетесь модератором'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied('Доступ запрещен. Пользователь не авторизован')
        if request.user.role == UserRoles.MODERATOR:
            return True
        return False


class IsCustomAdmin(BasePermission):
    message = 'Доступ запрещен. Вы не являетесь администратором'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied('Доступ запрещен. Пользователь не авторизован')
        if request.user.role == UserRoles.ADMINISTRATOR:
            return True
        return False
