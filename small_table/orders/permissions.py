from rest_framework import permissions


class IsOrderOwnerOrVendor(permissions.BasePermission):
    """
    הרשאה מותאמת:
    - לקוח יכול לראות/לערוך רק הזמנות שלו
    - ספק יכול לראות/לערוך הזמנות שהוזמנו ממנו
    - רק הספק יכול לעדכן את הסטטוס
    """

    def has_object_permission(self, request, view, obj):
        """
        בדיקת הרשאה על אובייקט ספציפי (הזמנה מסוימת).
        """
        user = request.user

        # בדיקה אם המשתמש הוא בעל ההזמנה
        if obj.user == user:
            # לקוח יכול לראות ולערוך את ההזמנה שלו (אבל לא את הסטטוס)
            if request.method in permissions.SAFE_METHODS:
                # GET, HEAD, OPTIONS - מותר
                return True

            # PUT, PATCH - מותר רק אם לא מנסה לשנות סטטוס
            if 'status' in request.data:
                return False
            return True

        # בדיקה אם המשתמש הוא הספק של ההזמנה
        if hasattr(user, 'vendor_profile') and obj.vendor == user.vendor_profile:
            # ספק יכול לראות ולעדכן הכל (כולל סטטוס)
            return True

        # אחרת - אין הרשאה
        return False


class IsVendorOrReadOnly(permissions.BasePermission):
    """
    הרשאה פשוטה:
    - כולם יכולים לקרוא (GET)
    - רק ספק יכול לכתוב (POST, PUT, PATCH, DELETE)
    """

    def has_permission(self, request, view):
        """
        בדיקת הרשאה כללית.
        """
        # קריאה - מותר לכולם
        if request.method in permissions.SAFE_METHODS:
            return True

        # כתיבה - רק לספקים
        return hasattr(request.user, 'vendor_profile')