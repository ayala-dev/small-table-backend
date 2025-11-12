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

#רשימת כלים שמאפשרים להוסיף פילטירים
    filter_backends = [ DjangoFilterBackend,  filters.SearchFilter,  filters.OrderingFilter  ]
   #הגדרת השדות שפתוחות לפילטור

    search_fields = [#אילו שדות נכללים בחיפוש
        'business_name',
        'kashrut_level',
        'address',
        'user__username',
        'user__email'
    ]
    ordering_fields = [# אילו שדות מותר למיין לפיהם
        'business_name',
        'created_at',
        'is_active'
    ]
    ordering = ['-created_at']  # ברירת מחדל:
   #קובע באופן דינמי איזה מההרשאות יבדקו עבור כל פעולה
    def get_permissions(self):

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


        user = self.request.user
        # אם המשתמש הוא מנהל (admin/superuser) - רואה הכול
        if user.is_staff or user.is_superuser:
         return queryset

        # כל השאר - רואים רק ספקים פעילים
        return queryset.filter(is_active=True)


#דריסת פונקצית המקור והוספת ולדציה של לוגיקה עסקית
    def create(self, request, *args, **kwargs):
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

    #בהמשך הרחבת הפונקציות של ה-ViewSet
def perform_create(self, serializer):
    vendor = serializer.save()

    print(f" ספק נרשם: {vendor.business_name}")

def perform_update(self, serializer):
    vendor = serializer.save()
    print(f"✏️ ספק עודכן: {vendor.business_name}")

def perform_destroy(self, instance):
    print(f"🗑️ ספק נמחק: {instance.business_name} (ID: {instance.id})")
    instance.delete()
