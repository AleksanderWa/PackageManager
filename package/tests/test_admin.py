from decimal import Decimal

from django.contrib.admin import AdminSite
from django.test import TestCase

from package.admin import OrderAdmin
from package.factory import FurnitureFactory, OrderFactory, OrderItemFactory, PackageFactory
from package.models import Order


class MockRequest(object):
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


request = MockRequest()
request.user = MockSuperUser()


class OrderAdminTest(TestCase):
    def setUp(self):
        super().setUp()
        self.app_admin = OrderAdmin(Order, AdminSite())

    def create_order_fixture(self, furniture_weight, furniture_price, package1_weight, package2_weight):
        furniture = FurnitureFactory.create(price=furniture_price, weight=furniture_weight)

        PackageFactory.create(furniture=furniture, weight=package1_weight)
        PackageFactory.create(furniture=furniture, weight=package2_weight)

        order = OrderFactory.create()
        for _ in range(0, 2):
            OrderItemFactory.create(order=order, furniture=furniture)
        return order

    def test_correct_qs_annotations(self):

        order_1 = self.create_order_fixture(Decimal("17.50"), Decimal("199.99"), Decimal("15.00"), Decimal("5.00"))
        order_2 = self.create_order_fixture(Decimal("5.50"), Decimal("99.99"), Decimal("2.00"), Decimal("7.00"))

        queryset = self.app_admin.get_queryset(request)
        self.assertEqual(queryset.get(id=order_1.id)._furniture_weight, Decimal("35.00"))
        self.assertEqual(queryset.get(id=order_1.id)._total_packages, 4)
        self.assertEqual(queryset.get(id=order_1.id)._packages_weight, Decimal("40.00"))

        self.assertEqual(queryset.get(id=order_2.id)._furniture_weight, Decimal("11.00"))
        self.assertEqual(queryset.get(id=order_2.id)._total_packages, 4)
        self.assertEqual(queryset.get(id=order_2.id)._packages_weight, Decimal("18.00"))
