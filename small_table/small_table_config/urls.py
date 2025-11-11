from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/vendors/', include('vendors.urls')),
    path('api/', include('products.urls')),
    path('api/packages/', include('packages.urls')),
    path('api/addons/', include('addons.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/qna/', include('qna.urls')),
    path('api/roles/', include('roles.urls')),
    path('api/user-roles/', include('user_roles.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
