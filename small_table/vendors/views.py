from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import VendorProfile
from .serializers import VendorProfileSerializer
from .permissions import IsVendorOwnerOrAdmin

class VendorProfileViewSet(viewsets.ModelViewSet):
   # ViewSet לניהול פרופילי ספקים

    queryset = VendorProfile.objects.select_related('user').all()
    serializer_class = VendorProfileSerializer

    filter_backends = [
        DjangoFilterBackend,  # סינון מדויק
        filters.SearchFilter,  # חיפוש טקסט
        filters.OrderingFilter  # מיון
    ]
    search_fields = [
        'business_name',
        'kashrut_level',
        'address',
        'user__username',
        'user__email'
    ]
    ordering_fields = [
        'business_name',
        'created_at',
        'is_active'
    ]
    ordering = ['-created_at']  # ברירת מחדל:
    def get_permissions(self):

        # 🔐 אבטחה - Principle of Least Privilege
       # כל פעולה מקבלת רק את ההרשאות המינימליות הנדרשות
       #  ──────────────────────────────────────────────────────────
       #  📖 קריאה (GET) - כולם
       #  ──────────────────────────────────────────────────────────
        if self.action in ['list', 'retrieve']:
           permission_classes = [IsAuthenticatedOrReadOnly]
        #  ──────────────────────────────────────────────────────────
        # ➕ יצירה (POST) - רק מחובר
        # ──────────────────────────────────────────────────────────
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
       # ──────────────────────────────────────────────────────────
       #  ✏️🗑️ עריכה/מחיקה - רק בעלים או מנהל
       # ──────────────────────────────────────────────────────────
        elif self.action in ['update', 'partial_update', 'destroy']:
           permission_classes = [IsAuthenticated, IsVendorOwnerOrAdmin]


     #   ברירת מחדל: רק מחובר (Fail Secure)

        else:
           permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):

      #  סינון חכם של רשימת ספקים

        queryset = super().get_queryset()

        queryset = queryset.filter(is_active=True)

        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(address__icontains=city)

        return queryset


    def create(self, request, *args, **kwargs):
        """
        יצירת ספק חדש עם וולידציה נוספת
        """
        user_id = request.data.get('user')

        if VendorProfile.objects.filter(user_id=user_id).exists():
            return Response(
                {
                    'error': 'משתמש זה כבר רשום כספק במערכת',
                    'detail': 'כל משתמש יכול להיות רק ספק אחד'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # יצירה רגילה
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        vendor = serializer.save()

        print("ספק חדש: {} (משתמש: {})".format(
            vendor.business_name,
            vendor.user.username
        ))

        # 💡 בעתיד: שליחת מייל, התראות


    def perform_update(self, serializer):

        vendor = serializer.save()


        print("✏️ ספק עודכן: {vendor.business_name}")



def perform_destroy(self, instance):

        print("🗑️ ספק נמחק: {instance.business_name} (ID: {instance.id})")

        # מחיקה בפועל
        instance.delete()