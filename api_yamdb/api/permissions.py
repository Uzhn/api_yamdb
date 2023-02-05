from rest_framework import permissions


class IsSuperUserOrIsAdmin(permissions.BasePermission):
    """Пермишн, является ли пользователь супер юзером или админом."""

    message = 'У вас нет прав администратора или суперпользователя.'

    def has_permission(self, request, view):
        return (request.user.is_superuser or request.user.is_admin)


class IsAnonimUser(permissions.BasePermission):
    """Разрешает анонимному пользователю только безопасные запросы."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsModerator(permissions.BasePermission):
    """Пермишн является ли пользователь модератором."""

    def has_permission(self, request, view):
        return (request.user.is_moderator)
