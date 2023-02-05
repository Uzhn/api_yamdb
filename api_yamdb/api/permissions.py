from rest_framework import permissions


class IsSuperUserOrIsAdmin(permissions.BasePermission):
    """Пермишн, является ли пользователь супер юзером или админом."""

    message = 'У вас нет прав администратора или суперпользователя.'

    def has_permission(self, request, view):
        return (request.user.is_superuser or request.user.is_admin)
