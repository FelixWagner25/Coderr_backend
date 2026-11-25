from rest_framework import permissions


class IsUserTypeCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'customer'


class IsUserTypeBusinessUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'business'


class IsOrderBusinessUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.business_user


class IsReviewer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.reviewer


class IsObjectCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
