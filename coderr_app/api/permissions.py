from rest_framework import permissions
from coderr_app.models import User


class UserIsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'customer'
