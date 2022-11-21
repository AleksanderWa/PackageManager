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
    postal_code = factory.Faker("postcode")
    country = fuzzy.FuzzyChoice(["PL", "DE", "CH", "FR", "BE", "NL", "LU", "GB"])


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem


class PackageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Package

    number = factory.LazyAttribute(lambda o: "Numer: ".join(str(random.randint(1, 20))))
    weight = factory.LazyAttribute(
        lambda o: faker.pydecimal(min_value=1.00, max_value=5.00, left_digits=2, right_digits=2, positive=True)
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

        if extracted:
            packages_number = random.randint(4, 10)
            packages = PackageFactory.create_batch(packages_number, furniture=self)

            packages_weight = sum([package.weight for package in packages])
            self.weight = packages_weight
