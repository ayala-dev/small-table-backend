from django.db import models
from django.conf import settings


class Order(models.Model):
    """
    מייצג הזמנה של לקוח מול ספק.
    """

    # קשר למשתמש שביצע את ההזמנה
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    # קשר לספק
    vendor = models.ForeignKey(
        'vendors.VendorProfile',
        on_delete=models.CASCADE,
        related_name='orders'
    )

    # קשר לחבילה שנבחרה
    """package = models.ForeignKey(
        'packages.Package',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )"""


    # סוג החבילה שנבחרה בהזמנה
    package_type = models.CharField(
        max_length=20,
        choices=[
            ('ready', 'חבילה מוכנה'),
            ('custom', 'חבילה מותאמת'),
        ]
    )

    # מספר סועדים
    guests_count = models.IntegerField()

    # סטטוס ההזמנה
    status = models.CharField(
        max_length=50,
        choices=[
            ('new', 'חדש'),
            ('processing', 'בתהליך'),
            ('completed', 'הושלם'),
            ('cancelled', 'בוטל'),
        ],
        default='new'
    )

    # מחיר כולל
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # הערות להזמנה
    note = models.TextField(blank=True, null=True)

    # תאריכים
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} -> {self.vendor.business_name}"


class OrderItem(models.Model):
    """
    פריט בהזמנה - מקשר בין הזמנה למוצר.
    מאפשר לשמור כמה מנות מכל סוג הוזמנו.
    """

    # קשר להזמנה
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    # קשר למוצר
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,  # לא למחוק מוצר אם יש לו הזמנות
        related_name='order_items'
    )

    # כמות
    quantity = models.IntegerField(default=1)

    # מחיר ליחידה בזמן ההזמנה (snapshot - גם אם המחיר ישתנה בעתיד)
    price_snapshot = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="מחיר המוצר בזמן ההזמנה"
    )

    # תוספת מחיר (למנה משודרגת)
    extra_price_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="תוספת מחיר אם זו מנה משודרגת"
    )

    # תאריך יצירה
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "פריט בהזמנה"
        verbose_name_plural = "פריטים בהזמנות"
        ordering = ['id']

    def __str__(self):
        return f"{self.product.name} x{self.quantity} (הזמנה #{self.order.id})"

    @property
    def subtotal(self):
        """
        חישוב סכום חלקי לפריט זה.
        """
        return (self.price_snapshot + self.extra_price_per_person) * self.quantity