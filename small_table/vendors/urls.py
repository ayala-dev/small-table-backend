from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorProfileViewSet


# ──────────────────────────────────────────────────────────────
# 🔧 יצירת Router אוטומטי
# ──────────────────────────────────────────────────────────────
router = DefaultRouter()

# רישום ה-ViewSet תחת הנתיב 'vendors'
# basename מאפשר ל-Django לזהות את ה-ViewSet בשם ייחודי
router.register(
    r'vendors',                    # הנתיב ב-URL
    VendorProfileViewSet,          # ה-ViewSet שיטפל בבקשות
    basename='vendor'              # שם בסיס לשימוש ב-reverse()
)

urlpatterns = [
    path('', include(router.urls)),
]
