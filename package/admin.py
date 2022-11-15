from django.contrib import admin, messages
from django.db.models import Subquery, Sum
from django.db.models.functions import Coalesce

from package.models import Order


class TotalPackagesFilter(admin.SimpleListFilter):
    title = "total_packages_filter"
    parameter_name = "total_packages_filter"

    def lookups(self, request, model_admin):
        return (
            ("1", "1"),
            ("2", "2"),
            ("5", "5"),
            ("10", "10"),
            ("10", "10+"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value in ("1", "2", "5", "10"):
            queryset = queryset.filter(_total_packages=value)
        elif value in ("10+",):
            queryset = queryset.filter(_total_packages__gt=value)
        return queryset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        furniture_weight = Order.objects.all().annotate(_furniture_weight=Sum("items__furniture__weight"))
        # total_package = Order.objects.all().annotate(_total_packages=Count("items__furniture__packages"))
        packages_weight = Order.objects.all().annotate(_furniture_weight=Sum("items__furniture__packages__weight"))
        return Order.objects.all().annotate(
            _furniture_weight=Coalesce(Subquery(furniture_weight), 0),
            _total_packages=Coalesce(Subquery(packages_weight), 0),
        )

    list_display = ("id", "created_at", "customer_name", "country", "status", "furniture_weight", "total_packages")
    list_filter = ("status", TotalPackagesFilter)
    actions = ["count_weight"]

    def packages_weight(self, obj):
        return obj._packages_weight

    def furniture_weight(self, obj):
        return obj._furniture_weight

    def total_packages(self, obj):
        return obj._total_packages

    packages_weight.admin_order_field = "_packages_weight"
    furniture_weight.admin_order_field = "_furniture_weight"
    total_packages.admin_order_field = "_total_packages"

    def count_weight(self, request, queryset):
        weight = queryset.aggregate(Sum("_furniture_weight"))["_furniture_weight__sum"]
        messages.add_message(request, messages.INFO, f"Weight in kg: {weight}")
