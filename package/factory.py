import random

import factory
from factory import fuzzy
from faker import Faker

from package.models import Furniture, Order, OrderItem, Package

faker = Faker()


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer_name = factory.Faker("name")
    country = fuzzy.FuzzyChoice(["PL", "DE", "CH", "FR", "BE", "NL", "LU", "GB"])


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    quantity = factory.LazyAttribute(lambda o: faker.pyint(min_value=50, max_value=10000, step=1.5))


class PackageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Package

    number = factory.LazyAttribute(lambda o: "Numer: ".join(str(random.randint(1, 20))))
    weight = factory.LazyAttribute(
        lambda o: faker.pydecimal(min_value=2.00, max_value=20.00, left_digits=2, right_digits=2, positive=True)
    )


class FurnitureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Furniture

    name = fuzzy.FuzzyChoice(["Chair", "Wardrobe 10x10", "Wardrobe 5x5", "Bed"])
    weight = factory.LazyAttribute(
        lambda o: faker.pydecimal(min_value=2.00, max_value=20.00, left_digits=2, right_digits=2, positive=True)
    )
    price = factory.LazyAttribute(
        lambda o: faker.pydecimal(min_value=2.00, max_value=20.00, left_digits=2, right_digits=2, positive=True)
    )

    @factory.post_generation
    def with_packages(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        packages_number = random.randint(4, 10)
        packages = PackageFactory.create_batch(packages_number, furniture=self)

        furniture_weight = sum([package.weight for package in packages])
        self.weight = furniture_weight
