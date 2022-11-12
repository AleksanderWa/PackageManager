from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("modified at"), auto_now=True)

    class Meta:
        abstract = True


class ProductModel(models.Model):
    name = models.CharField(verbose_name="name", max_length=40, null=True)
    weight = models.DecimalField(verbose_name="weight", default=0, decimal_places=2, max_digits=5)

    class Meta:
        abstract = True


class Furniture(TimestampModel, ProductModel):
    # name = models.CharField(verbose_name="name", max_length=40, null=True)
    # weight = models.DecimalField(verbose_name="weight", default=0, decimal_places=2, max_digits=5)

    class Meta:
        verbose_name = _("furniture")
        verbose_name_plural = _("furnitures")


class Package(TimestampModel, ProductModel):
    # weight = models.DecimalField(verbose_name="weight", default=0, decimal_places=2, max_digits=5)
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name="packages")

    class Meta:
        verbose_name = _("package")
        verbose_name_plural = _("packages")


class Order(TimestampModel):
    customer_name = models.CharField(verbose_name="customer name", max_length=30, null=True)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")


class OrderItem(TimestampModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    furniture = models.ForeignKey(Furniture, on_delete=models.PROTECT)
    quantity = models.IntegerField(verbose_name="quantity")

    class Meta:
        verbose_name = _("order item")
        verbose_name_plural = _("order items")
