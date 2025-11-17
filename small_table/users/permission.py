from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    רק המשתמש עצמו או מי שתפקידו 'admin' יכול לערוך או למחוק משתמש.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if getattr(user, 'role', None) and getattr(user.role, 'name', None) == 'admin':
            return True
        return obj == user
