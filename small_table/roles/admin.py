from django.contrib import admin
from .models import Role

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    ניהול טבלת Role בממשק האדמין
    """
    list_display = ['id', 'name']     # אילו עמודות יוצגו בטבלה
    search_fields = ['name']          # שדה חיפוש לפי שם תפקיד
    ordering = ['id']                 # סדר ברירת מחדל
