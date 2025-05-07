from rest_framework import permissions


class IsModer(permissions.BasePermission):
    message = 'Adding customers not allowed'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()


class IsOwner(permissions.BasePermission):
    message = 'Adding customers not allowed'

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        else:
            return False


class IsProfileOwner(permissions.BasePermission):
    message = 'You can only edit your own profile'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
