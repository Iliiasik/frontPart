from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdminOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method == 'GET':
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user == obj.owner or request.user.is_staff


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and request.user.is_staff:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_staff


class CanCreateUpdateDeleteTicket(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class CanInteractWithTicket(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
