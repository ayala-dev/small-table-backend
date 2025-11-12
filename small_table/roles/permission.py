from rest_framework import permissions

class IsAdminOnlyCanEdit(permissions.BasePermission):
    """
    רק מנהל יכול לשנות או למחוק תפקידים.
    כל השאר יכולים רק לצפות.
    """

    def has_permission(self, request, view):
        # אם המשתמש לא מחובר – אסור לגמרי
        if not request.user.is_authenticated:
            return False

        # לצפייה בלבד מותר לכולם
        if request.method in permissions.SAFE_METHODS:
            return True

        # לשינוי מותר רק אם המשתמש מנהל (is_staff או is_superuser)
        return request.user.is_staff or request.user.is_superuser
