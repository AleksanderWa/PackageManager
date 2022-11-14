from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from package.factory import FurnitureFactory, OrderFactory
from package.models import Furniture, Order, OrderItem, Package


class BaseTestCase(TestCase):
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
        quantity = 15
        order_item = OrderItem.objects.create(quantity=quantity, furniture=furniture, order=order)
        order_item.refresh_from_db()
        self.assertEqual(order_item.quantity, quantity)
        self.assertEqual(order_item.furniture, furniture)
        self.assertEqual(order_item.order, order)

    def test_cant_create_order_item_without_order(self):
        furniture = FurnitureFactory.create()
        quantity = 15
        with self.assertRaises(IntegrityError):
            OrderItem.objects.create(quantity=quantity, furniture=furniture)

    def test_can_create_order(self):
        customer_name = "Spider Man"
        order = Order.objects.create(customer_name=customer_name)
        order.refresh_from_db()
        self.assertEqual(Order.objects.filter(id=order.id).exists(), True)
        self.assertEqual(order.customer_name, customer_name)
