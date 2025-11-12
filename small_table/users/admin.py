from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    ממשק ניהול לפרופילי משתמשים ב-Django Admin
    """
    list_display = [
        'first_name',
        'last_name',
        'email',
        'phone',
        'is_staff',
        'is_active',
        'date_joined',
    ]
    list_filter = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']
    readonly_fields = ['date_joined', 'is_active']
