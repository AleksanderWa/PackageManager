from decimal import Decimal

from django.contrib.admin import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpRequest
from django.test import TestCase

from package.admin import OrderAdmin, OrderItemAdmin
from package.factory import FurnitureFactory, OrderFactory, OrderItemFactory, PackageFactory
from package.models import Order, OrderItem


class MockRequest(object):
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


request = HttpRequest()
request.user = MockSuperUser()
setattr(request, "session", "session")
setattr(request, "_messages", FallbackStorage(request))


class BaseAdminTest(TestCase):
    def create_order_fixture(self, furniture_weight, furniture_price, package1_weight, package2_weight):
        furniture = FurnitureFactory.create(price=furniture_price, weight=furniture_weight)

        PackageFactory.create(furniture=furniture, weight=package1_weight)
        PackageFactory.create(furniture=furniture, weight=package2_weight)

        order = OrderFactory.create()
        for _ in range(0, 2):
            OrderItemFactory.create(order=order, furniture=furniture)
        return order


class OrderAdminTest(BaseAdminTest):
    def setUp(self):
        super().setUp()
        self.app_admin = OrderAdmin(Order, AdminSite())

    def test_correct_queryset_annotations(self):

        order_1 = self.create_order_fixture(
            furniture_weight=Decimal("17.50"),
            furniture_price=Decimal("199.99"),
            package1_weight=Decimal("15.00"),
            package2_weight=Decimal("5.00"),
        )
        order_2 = self.create_order_fixture(
            furniture_weight=Decimal("5.50"),
            furniture_price=Decimal("99.99"),
            package1_weight=Decimal("2.00"),
            package2_weight=Decimal("7.00"),
        )

        queryset = self.app_admin.get_queryset(request)
        self.assertEqual(queryset.get(id=order_1.id)._furniture_weight, Decimal("35.00"))
        self.assertEqual(queryset.get(id=order_1.id)._total_packages, 4)
        self.assertEqual(queryset.get(id=order_1.id)._packages_weight, Decimal("40.00"))

        self.assertEqual(queryset.get(id=order_2.id)._furniture_weight, Decimal("11.00"))
        self.assertEqual(queryset.get(id=order_2.id)._total_packages, 4)
        self.assertEqual(queryset.get(id=order_2.id)._packages_weight, Decimal("18.00"))

    def test_bulk_send_status_changed(self):
        request.method = "POST"
        request.POST = {"apply": "Submit", "delivery_company": "DPD"}
        self.create_order_fixture(Decimal("17.50"), Decimal("199.99"), Decimal("15.00"), Decimal("5.00"))
        self.create_order_fixture(Decimal("5.50"), Decimal("99.99"), Decimal("2.00"), Decimal("7.00"))

        queryset = self.app_admin.get_queryset(request)
        self.app_admin.bulk_send(request, queryset)
        statuses = list(queryset.values_list("status", flat=True))
        for status in statuses:
            self.assertEqual(status, Order.Status.READY_TO_SEND)

    def test_bulk_send_validation_error_status_not_changed(self):
        request.method = "POST"
        request.POST = {"apply": "Submit", "delivery_company": "blablabla"}
        self.create_order_fixture(Decimal("17.50"), Decimal("199.99"), Decimal("15.00"), Decimal("5.00"))
        self.create_order_fixture(Decimal("5.50"), Decimal("99.99"), Decimal("2.00"), Decimal("7.00"))

        queryset = self.app_admin.get_queryset(request)
        self.app_admin.bulk_send(request, queryset)
        statuses = list(queryset.values_list("status", flat=True))
        for status in statuses:
            self.assertEqual(status, Order.Status.NEW)

    def test_bulk_send_GET_status_not_changed(self):
        request.method = "GET"
        request.POST = {"apply": "Submit", "delivery_company": "DPD"}
        self.create_order_fixture(Decimal("17.50"), Decimal("199.99"), Decimal("15.00"), Decimal("5.00"))
        self.create_order_fixture(Decimal("5.50"), Decimal("99.99"), Decimal("2.00"), Decimal("7.00"))

        queryset = self.app_admin.get_queryset(request)
        self.app_admin.bulk_send(request, queryset)
        statuses = list(queryset.values_list("status", flat=True))
        for status in statuses:
            self.assertEqual(status, Order.Status.NEW)


class OrderItemAdminTest(BaseAdminTest):
    def setUp(self):
        super().setUp()
        self.app_admin = OrderItemAdmin(OrderItem, AdminSite())

    def test_correct_queryset_annotations(self):
        """
        2 orders
        1:    2 order_items = (2x furniture = 4 packages)
        2:   2 order_items = (2x furniture = 4 packages)
        """
        order_1 = self.create_order_fixture(
            furniture_weight=Decimal("17.50"),
            furniture_price=Decimal("199.99"),
            package1_weight=Decimal("15.00"),
            package2_weight=Decimal("5.00"),
        )
        order_2 = self.create_order_fixture(
            furniture_weight=Decimal("5.50"),
            furniture_price=Decimal("99.99"),
            package1_weight=Decimal("2.00"),
            package2_weight=Decimal("7.00"),
        )

        queryset = self.app_admin.get_queryset(request)
        order_1_items_packages = list(queryset.filter(order=order_1).values_list("_total_packages", flat=True))
        order_2_items_packages = list(queryset.filter(order=order_2).values_list("_total_packages", flat=True))

        for packages in (*order_1_items_packages, *order_2_items_packages):
            self.assertEqual(packages, 2)

        order_1_packages_weight = list(queryset.filter(order=order_1).values_list("_packages_weight", flat=True))
        self.assertEqual(set(order_1_packages_weight), {Decimal("20.00"), Decimal("20.00")})

        order_2_packages_weight = list(queryset.filter(order=order_2).values_list("_packages_weight", flat=True))
        self.assertEqual(set(order_2_packages_weight), {Decimal("9.00"), Decimal("9.00")})

        order_1_furniture_weight = list(queryset.filter(order=order_1).values_list("_furniture_weight", flat=True))
        self.assertEqual(set(order_1_furniture_weight), {Decimal("17.50"), Decimal("17.50")})

        order_2_furniture_weight = list(queryset.filter(order=order_2).values_list("_furniture_weight", flat=True))
        self.assertEqual(set(order_2_furniture_weight), {Decimal("5.50"), Decimal("5.50")})

    # def test_row_style_for_benelux_country(self):
    #     poland_order = OrderFactory.create(country="PL")
    #     OrderItemFactory.create()
    #     self.app_admin.set_row_style()
