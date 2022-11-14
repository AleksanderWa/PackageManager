from django.contrib import admin

from package.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "country", "status", "total_packages", "packages_weight", "furniture_weight")
