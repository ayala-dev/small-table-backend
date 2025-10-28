from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/vendors/', include('vendors.urls')),
    path('api/products/', include('products.urls')),
    path('api/packages/', include('packages.urls')),
    path('api/addons/', include('addons.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/qna/', include('qna.urls')),
    path('api/', include('api.urls')),
]
