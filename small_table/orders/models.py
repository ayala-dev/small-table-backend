from django.db import models
from django.conf import settings


class Order(models.Model):
    """
    הזמנה המבוססת על חבילה מוכנה בלבד.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    vendor = models.ForeignKey(
        'vendors.VendorProfile',
        on_delete=models.PROTECT,
        related_name='orders'
    )

    package = models.ForeignKey(
        'packages.Package',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )

    guests_count = models.PositiveIntegerField()

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

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "הזמנה"
        verbose_name_plural = "הזמנות"

    def __str__(self):
        return f"הזמנה #{self.id} ({self.user.username})"


class OrderItem(models.Model):
    """
    פריט הזמנה – מבוסס רק על קטגוריות החבילה.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    package_category = models.ForeignKey(
        'packages.PackageCategory',
        on_delete=models.PROTECT,
        related_name='order_items'
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='order_items'
    )

    quantity = models.PositiveIntegerField(default=1)

    price_snapshot = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="מחיר המנה בזמן ההזמנה"
    )

    extra_price_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "פריט הזמנה"
        verbose_name_plural = "פריטי הזמנה"

    def __str__(self):
        return f"{self.product.product_name} (הזמנה {self.order.id})"
