from decimal import Decimal

from django.db import DataError, IntegrityError
from django.test import TestCase

from package.factory import FurnitureFactory, OrderFactory
from package.models import Furniture, Order, OrderItem, Package


class BaseTestCase(TestCase):
    def get_order_data(self):
        return {
            "customer_name": "Spider Man",
            "country": "PL",
            "status": Order.Status.SENT,
            "postal_code": "85-100",
            "province": "Pomorskie",
        }

    def test_can_create_furniture(self):
        price = Decimal("115.99")
        weight = Decimal("150.05")
        furniture = Furniture.objects.create(name="Wardrobe 5x5", price=price, weight=weight)
        furniture.refresh_from_db()
        self.assertEqual(Furniture.objects.filter(id=furniture.id).exists(), True)
        self.assertEqual(furniture.price, price)
        self.assertEqual(furniture.weight, weight)

    def test_can_create_package(self):
        furniture = FurnitureFactory.create()
        number = "Nmb 1/5"
        weight = Decimal("150.05")
        package = Package.objects.create(number=number, weight=weight, furniture=furniture)
        package.refresh_from_db()
        self.assertEqual(Package.objects.filter(id=package.id).exists(), True)
        self.assertEqual(package.number, number)
        self.assertEqual(package.weight, weight)
        self.assertEqual(package.furniture, furniture)

    def test_cant_create_packages_without_furniture(self):
        with self.assertRaises(IntegrityError):
            Package.objects.create(number="Nmb 1/5", weight=Decimal("10.05"))

    def test_can_create_order_item(self):
        furniture = FurnitureFactory.create()
        order = OrderFactory.create()
        order_item = OrderItem.objects.create(furniture=furniture, order=order)
        order_item.refresh_from_db()
        self.assertEqual(order_item.furniture, furniture)
        self.assertEqual(order_item.order, order)

    def test_cant_create_order_item_without_order(self):
        furniture = FurnitureFactory.create()
        with self.assertRaises(IntegrityError):
            OrderItem.objects.create(furniture=furniture)

    def test_can_create_order(self):
        data = self.get_order_data()
        order = Order.objects.create(**data)
        order.refresh_from_db()
        self.assertEqual(Order.objects.filter(id=order.id).exists(), True)
        self.assertEqual(order.customer_name, data["customer_name"])
        self.assertEqual(order.country, data["country"])
        self.assertEqual(order.status, data["status"])

    def test_cant_create_order_wrong_post_code(self):
        data = self.get_order_data()
        data["postal_code"] = "66992211"
        with self.assertRaises(DataError):
            Order.objects.create(**data)

    def test_furniture_factory_created_with_packages(self):
        furniture = FurnitureFactory.create(with_packages=True)
        furniture.refresh_from_db()
        self.assertEqual(furniture.packages.exists(), True)
