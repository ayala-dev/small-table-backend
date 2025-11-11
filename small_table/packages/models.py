from django.db import models


class Package(models.Model):
    """
    חבילה שספק מציע - גרסה בסיסית לספרינט 1.
    נרחיב בספרינט 2.
    """
    vendor = models.ForeignKey(
        'vendors.VendorProfile',
        on_delete=models.CASCADE,
        related_name='packages'
    )

    name = models.CharField(max_length=200, verbose_name='שם החבילה')
    description = models.TextField(blank=True, null=True, verbose_name='תיאור')
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='מחיר למנה')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'חבילה'
        verbose_name_plural = 'חבילות'

    def __str__(self):
        return f"{self.name} - {self.vendor.business_name}"


class PackageCategory(models.Model):
    """
    קטגוריה בתוך חבילה - גרסה בסיסית.
    """
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100, verbose_name='שם קטגוריה')

    class Meta:
        verbose_name = 'קטגוריה בחבילה'
        verbose_name_plural = 'קטגוריות בחבילות'

    def __str__(self):
        return f"{self.name} - {self.package.name}"