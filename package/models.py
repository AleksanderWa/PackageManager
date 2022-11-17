from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class TimestampModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("modified at"), auto_now=True)

    class Meta:
        abstract = True


class Furniture(TimestampModel):
    name = models.CharField(verbose_name=_("name"), max_length=40)
    weight = models.DecimalField(
        verbose_name=_("weight"), help_text=_("weight in kilograms"), default=0, decimal_places=2, max_digits=5
    )
    price = models.DecimalField(verbose_name=_("price"), default=0, decimal_places=2, max_digits=5)

    class Meta:
        verbose_name = _("furniture")
        verbose_name_plural = _("furnitures")


class Package(TimestampModel):
    number = models.CharField(verbose_name=_("number"), max_length=40)
    weight = models.DecimalField(
        verbose_name=_("weight"), help_text=_("weight in kilograms"), default=0, decimal_places=2, max_digits=5
    )
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name="packages")

    class Meta:
        verbose_name = _("package")
        verbose_name_plural = _("packages")


class Order(TimestampModel):
    class Status(models.IntegerChoices):
        NEW = 1, _("New")
        READY_TO_SEND = 2, _("Ready to send")
        SENT = 3, _("Sent")

    class Delivery(models.TextChoices):
        DPD = ("DPD",)
        FEDEX = ("Fedex",)
        UPS = ("UPS",)

    customer_name = models.CharField(verbose_name=_("customer name"), max_length=30)
    country = CountryField(null=False, blank=False)
    province = models.CharField(max_length=30, null=True)
    postal_code = models.CharField(
        null=True,
        max_length=6,
        validators=[RegexValidator("^[0-9]{6}$", _("Invalid postal code"))],
    )

    status = models.IntegerField(default=Status.NEW, choices=Status.choices)
    delivery_company = models.CharField(choices=Delivery.choices, blank=True, null=True, max_length=20)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def is_benelux_country(self):
        return self.country in ["BE", "NL", "LU"]


class OrderItem(TimestampModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    furniture = models.ForeignKey(Furniture, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("order item")
        verbose_name_plural = _("order items")
