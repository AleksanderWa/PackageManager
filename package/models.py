from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class TimestampModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("modified at"), auto_now=True)

    class Meta:
        abstract = True


class Furniture(TimestampModel):
    name = models.CharField(verbose_name="name", max_length=40)
    weight = models.DecimalField(
        verbose_name="weight", help_text="weight in kilograms", default=0, decimal_places=2, max_digits=5
    )
    price = models.DecimalField(verbose_name="price", default=0, decimal_places=2, max_digits=5)

    class Meta:
        verbose_name = _("furniture")
        verbose_name_plural = _("furnitures")


class Package(TimestampModel):
    number = models.CharField(verbose_name="number", max_length=40)
    weight = models.DecimalField(
        verbose_name="weight", help_text="weight in kilograms", default=0, decimal_places=2, max_digits=5
    )
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name="packages")

    class Meta:
        verbose_name = _("package")
        verbose_name_plural = _("packages")


class Order(TimestampModel):
    class Status(models.IntegerChoices):
        NEW = 1
        READY_TO_SEND = 2
        SENT = 3

    customer_name = models.CharField(verbose_name="customer name", max_length=30)
    country = CountryField(null=False, blank=False)
    status = models.IntegerField(default=Status.NEW, choices=Status.choices)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    # @property
    # def total_packages(self):
    #     return sum([order_item.furniture.packages.count() for order_item in self.items.all()])


class OrderItem(TimestampModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    furniture = models.ForeignKey(Furniture, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("order item")
        verbose_name_plural = _("order items")

    # @property
    # def packages_number(self):
    #     return self.furniture.packages.count()
    #
    # @property
    # def packages_weight(self):
    #     return sum([package.weight for package in self.furniture.packages.all()])
