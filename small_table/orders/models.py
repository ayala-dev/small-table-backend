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

    # ⭐ קשר לחבילה - יכול להיות NULL אם זו הרכבה אישית
    package = models.ForeignKey(
        'packages.Package',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        help_text='החבילה שנבחרה (NULL אם הרכבה אישית)'
    )

    package_type = models.CharField(
        max_length=20,
        choices=[
            ('ready', 'חבילה מוכנה'),
            ('custom', 'חבילה מותאמת'),
        ],
        help_text='ready = חבילה מוכנה מראש, custom = הרכבה אישית'
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

    class Meta:
        verbose_name = "הזמנה "
        verbose_name_plural = " הזמנות"
        ordering = ['created_at']


    def __str__(self):
        return f"Order #{self.id} - {self.user.username} -> {self.vendor.business_name}"
    @property
    def is_ready_package(self):
        """בדיקה אם זו חבילה מוכנה"""
        return self.package_type == 'ready' and self.package is not None

    @property
    def is_custom_package(self):
        """בדיקה אם זו הרכבה אישית"""
        return self.package_type == 'custom' and self.package is None

    def calculate_total(self):
        """חישוב מחיר כולל מכל הפריטים"""
        items_total = sum(item.subtotal for item in self.items.all())
        return items_total


class OrderItem(models.Model):
    """
    פריט בהזמנה - מקשר בין הזמנה למוצר.
    תומך גם בחבילה מוכנה וגם בהרכבה אישית.
    """

    # קשר להזמנה
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    # ⭐ קשר לקטגוריה בחבילה - NULL אם הרכבה אישית
    package_category = models.ForeignKey(
        'packages.PackageCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order_items',
        help_text='הקטגוריה בחבילה (NULL אם הרכבה אישית)'
    )

    # קשר למוצר
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='order_items'
    )

    # כמות
    quantity = models.IntegerField(default=1)

    # ⭐ מחיר המוצר בזמן ההזמנה (snapshot)
    price_snapshot = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='מחיר המוצר בזמן ההזמנה'
    )

    # ⭐ תוספת מחיר למנה משודרגת
    extra_price_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='תוספת מחיר אם זו מנה משודרגת'
    )

    # תאריך יצירה
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "פריט בהזמנה"
        verbose_name_plural = "פריטים בהזמנות"
        ordering = ['id']

    def __str__(self):
        if self.package_category:
            return f"{self.product.product_name} ({self.package_category.name}) - הזמנה #{self.order.id}"
        return f"{self.product.product_name} (הרכבה אישית) - הזמנה #{self.order.id}"

    @property
    def subtotal(self):
        """
        חישוב סכום חלקי לפריט זה.
        (price_snapshot + extra_price_per_person) × quantity × guests_count
        """
        # ⭐ טיפול ב-None values
        price = self.price_snapshot or 0
        extra = self.extra_price_per_person or 0
        qty = self.quantity or 1
        guests = self.order.guests_count or 1

        return (price + extra) * qty * guests
    @property
    def is_premium(self):
        """בדיקה אם זו מנה משודרגת"""
        return self.extra_price_per_person > 0