from django.contrib import admin
from .models import Order, OrderItem
from products.models import Product
from packages.models import PackageCategory

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('created_at', 'get_subtotal')
    fields = (
        'product',
        'package_category',
        'quantity',
        'price_snapshot',
        'extra_price_per_person',
        'get_subtotal',
    )

    # ⭐ סינון דינמי של חבילות לפי הספק שנבחר
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "package_category":
            # אם יש order_id בURL (עריכה)
            if request.resolver_match.kwargs.get('object_id'):
                order_id = request.resolver_match.kwargs['object_id']
                try:
                    order = Order.objects.get(id=order_id)
                    # הצג רק קטגוריות מהחבילה שנבחרה
                    if order.package:
                        kwargs["queryset"] = PackageCategory.objects.filter(
                            package=order.package
                        )
                    else:
                        kwargs["queryset"] = PackageCategory.objects.none()
                except Order.DoesNotExist:
                    pass

        if db_field.name == "product":
            # אם יש order_id בURL
            if request.resolver_match.kwargs.get('object_id'):
                order_id = request.resolver_match.kwargs['object_id']
                try:
                    order = Order.objects.get(id=order_id)
                    # הצג רק מוצרים של אותו ספק
                    kwargs["queryset"] = Product.objects.filter(
                        vendor=order.vendor
                    )
                except Order.DoesNotExist:
                    pass

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_subtotal(self, obj):
        if obj.id:
            return f"{obj.subtotal:.2f} ₪"
        return "-"

    get_subtotal.short_description = 'סכום חלקי'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'vendor',
        'package',
        'guests_count',
        'status',
        'total_price',
        'created_at',
    )

    list_filter = (
        'status',

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
    inlines = [OrderItemInline]
    ordering = ('-created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'package_category',
        'quantity',
        'price_snapshot',
        'extra_price_per_person',
        'get_subtotal',
        'get_is_premium',
    )

    list_filter = (

        'package_category',
        'created_at',
    )

    search_fields = (
        'order__id',
        'product__product_name',
        'order__user__username',
    )

    readonly_fields = ('created_at', 'get_subtotal')

    def get_subtotal(self, obj):
        return f"{obj.subtotal:.2f} ₪"

    get_subtotal.short_description = 'סכום חלקי'

    def get_is_premium(self, obj):
        return "✅ משודרג" if obj.is_premium else "רגיל"

    get_is_premium.short_description = 'סוג'