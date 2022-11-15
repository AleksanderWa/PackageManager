import logging
import random

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from package.factory import FurnitureFactory, OrderFactory, OrderItemFactory

logger = logging.getLogger(__name__)


class Command(
    BaseCommand,
):
    help = "Create fixtures"

    def handle(self, *args, **options):
        self.create_admin()
        self.create_single_cabinet_orders()
        self.create_double_cabinet_orders()
        self.create_other_cabinet_orders()

        logger.info("Fixtures successfully created!")

    def create_admin(self):
        self.admin = User.objects.create_superuser(username="admin")
        self.admin.set_password("password")
        self.admin.save()

        logger.info("User created!")

    def create_single_cabinet_orders(self):
        single_cabinet_orders = OrderFactory.create_batch(70)
        for order in single_cabinet_orders:
            self.seed_order(order, 1)
        logger.info("Created single cabinets")

    def create_double_cabinet_orders(self):
        double_cabinet_orders = OrderFactory.create_batch(20)
        for order in double_cabinet_orders:
            self.seed_order(order, 2)
        logger.info("Created double cabinets")

    def create_other_cabinet_orders(self):
        other_cabinet_orders = OrderFactory.create_batch(10)
        for order in other_cabinet_orders:
            self.seed_order(order)
        logger.info("Created other cabinets")

    @staticmethod
    def seed_order(order, cabinets_number=None):
        cabinets_number = random.randint(1, 15) or cabinets_number
        # packages_number = random.randint(4, 10)

        furniture = FurnitureFactory.create(with_packages=True)
        # PackageFactory.create_batch(packages_number, furniture=furniture)
        for _ in range(0, cabinets_number):
            OrderItemFactory.create(order=order, furniture=furniture)

        logger.info("{} seeded with data".format(order))
