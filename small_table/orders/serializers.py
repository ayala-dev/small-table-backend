from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer בסיסי להזמנות.
    """

    # שדות נוספים לתצוגה בלבד
    user_name = serializers.CharField(source='user.username', read_only=True)
    vendor_name = serializers.CharField(source='vendor.business_name', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'user_name',
            'vendor',
            'vendor_name',
            'package_type',
            'guests_count',
            'status',
            'total_price',
            'note',
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