from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from package.factory import FurnitureFactory, OrderFactory, OrderItemFactory, PackageFactory
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
        country = "PL"
        status = Order.Status.SENT
        order = Order.objects.create(customer_name=customer_name, country=country, status=status)
        order.refresh_from_db()
        self.assertEqual(Order.objects.filter(id=order.id).exists(), True)
        self.assertEqual(order.customer_name, customer_name)
        self.assertEqual(order.country, country)
        self.assertEqual(order.status, status)

    def test_order_item_correct_packages_count(self):
        furniture_1 = FurnitureFactory.create()
        PackageFactory.create_batch(2, furniture=furniture_1)
        order = OrderFactory.create()
        order_item_1 = OrderItemFactory.create(quantity=10, order=order, furniture=furniture_1)  # 20 packages
        self.assertEqual(order_item_1.packages_number, 20)

    def test_order_correct_packages_count(self):
        furniture_1 = FurnitureFactory.create()
        furniture_2 = FurnitureFactory.create()

        PackageFactory.create_batch(2, furniture=furniture_1)
        PackageFactory.create_batch(2, furniture=furniture_2)

        order = OrderFactory.create()
        OrderItemFactory.create(quantity=10, order=order, furniture=furniture_1)  # 20 packages
        OrderItemFactory.create(quantity=5, order=order, furniture=furniture_2)  # 10 packages
        self.assertEqual(order.total_packages, 30)

    def test_furniture_factory_created_with_packages(self):
        furniture = FurnitureFactory.create(with_packages=True)
        furniture.refresh_from_db()
        self.assertEqual(furniture.packages.exists(), True)
