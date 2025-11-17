from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    category_name = serializers.CharField(source='package_category.name', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'product_name',
            'product_image',
            'package_category',
            'category_name',
            'quantity',
            'price_snapshot',
            'extra_price_per_person',
            'subtotal',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'subtotal',
            'created_at',
        ]

    def get_subtotal(self, obj):
        return (obj.price_snapshot + obj.extra_price_per_person) * obj.quantity


class OrderSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    vendor_name = serializers.CharField(source='vendor.business_name', read_only=True)
    package_name = serializers.CharField(source='package.name', read_only=True)

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'user_name',
            'vendor',
            'vendor_name',
            'package',
            'package_name',
            'guests_count',
            'status',
            'total_price',
            'note',
            'items',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_total_price(self, value):
        if value < 0:
            raise serializers.ValidationError("המחיר הכולל לא יכול להיות שלילי.")
        return value
