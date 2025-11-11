from rest_framework import serializers
from .models import Order
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer לפריטי הזמנה.
    """
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    category_name = serializers.CharField(source='package_category.name', read_only=True, allow_null=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_premium = serializers.BooleanField(read_only=True)

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
            'is_premium',
            'created_at',
        ]
        read_only_fields = ['id', 'subtotal', 'is_premium', 'created_at']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("הכמות חייבת להיות חיובית.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer בסיסי להזמנות.
    """

    # שדות נוספים לתצוגה בלבד
    user_name = serializers.CharField(source='user.username', read_only=True)
    vendor_name = serializers.CharField(source='vendor.business_name', read_only=True)
    package_name = serializers.CharField(source='package.name', read_only=True, allow_null=True)

    # ⭐ הוספת פריטי ההזמנה
    items = OrderItemSerializer(many=True, read_only=True)
    is_ready_package = serializers.BooleanField(read_only=True)
    is_custom_package = serializers.BooleanField(read_only=True)

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
            'package_type',
            'is_ready_package',
            'is_custom_package',
            'guests_count',
            'status',
            'total_price',
            'note',
            'items',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']



def validate_total_price(self, value):
        """
        בדיקה שהמחיר חיובי.
        """
        if value < 0:
            raise serializers.ValidationError("המחיר הכולל לא יכול להיות שלילי.")
        return value


def validate(self, data):
    """
    ולידציות כלליות.
    """
    package = data.get('package')
    package_type = data.get('package_type')

    # בדיקה: חבילה מוכנה חייבת להכיל package
    if package_type == 'ready' and not package:
        raise serializers.ValidationError({
            "package": "חבילה מוכנה חייבת להכיל חבילה."
        })

    # בדיקה: הרכבה אישית לא צריכה package
    if package_type == 'custom' and package:
        raise serializers.ValidationError({
            "package": "הרכבה אישית לא צריכה חבילה."
        })

    return data
