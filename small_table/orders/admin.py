from django.contrib import admin
from .models import Order
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'vendor',
       # 'package',
        'package_type',
        'guests_count',
        'status',
        'total_price',
        'created_at',
    )

    list_filter = (
        'status',
        'package_type',
        'vendor',
        'created_at',
    )

    search_fields = (
        'id',
        'user__username',
        'vendor__business_name',
        'package__name',
    )

    readonly_fields = ('created_at',)

    ordering = ('-created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
        list_display = (
            'id',
            'order',
            'product',
            'quantity',
            'price_snapshot',
            'extra_price_per_person',
            'get_subtotal',
        )

        list_filter = (
            'order__status',
            'product__vendor',
            'created_at',
        )

        search_fields = (
            'order__id',
            'product__name',
            'order__user__username',
        )

        readonly_fields = ('created_at', 'get_subtotal')

        def get_subtotal(self, obj):
            """
            הצגת סכום חלקי ב-Admin.
            """
            return f"{obj.subtotal:.2f} ₪"

        get_subtotal.short_description = 'סכום חלקי'

