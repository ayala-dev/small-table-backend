from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Order
from .serializers import OrderSerializer
from .permissions import IsOrderOwnerOrVendor


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet בסיסי לניהול הזמנות עם סינונים ומיונים.
    """
    queryset = Order.objects.select_related('user', 'vendor').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwnerOrVendor]

    # הוספת סינונים, חיפוש ומיון
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # שדות לסינון
    filterset_fields = ['status', 'package_type', 'vendor']

    # שדות לחיפוש
    search_fields = ['user__username', 'vendor__business_name', 'note']

    # שדות למיון
    ordering_fields = ['created_at', 'total_price', 'guests_count', 'status']
    ordering = ['-created_at']  # מיון ברירת מחדל

    def get_queryset(self):
        """
        מחזיר הזמנות לפי המשתמש המחובר.
        """
        user = self.request.user

        # ספק רואה את כל ההזמנות שהוזמנו ממנו
        if hasattr(user, 'vendor_profile'):
            return Order.objects.filter(
                vendor=user.vendor_profile
            ).select_related('user', 'vendor').order_by('-created_at')

        # לקוח רגיל רואה רק את ההזמנות שלו
        return Order.objects.filter(
            user=user
        ).select_related('user', 'vendor').order_by('-created_at')

    def perform_create(self, serializer):
        """
        בזמן יצירת הזמנה חדשה - מגדיר אוטומטי את המשתמש המחובר.
        """
        serializer.save(user=self.request.user, status='new')