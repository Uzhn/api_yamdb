
from rest_framework import permissions


class IsSuperUserOrIsAdmin(permissions.BasePermission):
    """Пермишн, является ли пользователь супер юзером или админом."""

    message = 'У вас нет прав администратора или суперпользователя.'

    def has_permission(self, request, view):
        return (request.user.is_superuser or request.user.is_admin)


class UserAuthOrModOrAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ('list', 'retrieve'):
            return request.method in permissions.SAFE_METHODS
        else:
            return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            return bool((obj.author == request.user and request.user.is_user)
                        or request.user.is_moderator or request.user.is_admin)
        elif request.method in permissions.SAFE_METHODS:
            return True


class Other(permissions.BasePermission):

    def has_permission(self, request, view):
        return ((request.method in permissions.SAFE_METHODS)
                or (request.user.is_authenticated and request.user.is_admin)
                or (request.user.is_authenticated
                    and request.user.is_superuser)
                )

    def has_object_permission(self, request, view, obj):
        return ((request.method in permissions.SAFE_METHODS)
                or request.user.is_admin
                or request.user.is_superuser
                )
