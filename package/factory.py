import random

import factory
from faker import Faker

from package.models import Furniture, Order, OrderItem, Package

faker = Faker()


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer_name = factory.Faker("name")
    #
    # @factory.post_generation
    # def records(self, create, extracted, **kwargs):
    #     if not create:
    #         # Simple build, do nothing.
    #         return
    #
    #     if extracted:
    #         # A list of groups were passed in, use them
    #         for budget_record in extracted:
    #             self.records.add(budget_record)
    #
    # @factory.post_generation
    # def owners(self, create, extracted, **kwargs):
    #     if not create:
    #         # Simple build, do nothing.
    #         return
    #
    #     if extracted:
    #         # A list of groups were passed in, use them
    #         for owner in extracted:
    #             self.owners.add(owner)


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

    name = random.choice(["Chair", "Wardrobe 10x10", "Wardrobe 5x5", "Bed"])
    weight = factory.LazyAttribute(
        lambda o: faker.pydecimal(min_value=2.00, max_value=20.00, left_digits=2, right_digits=2, positive=True)
    )
    price = factory.LazyAttribute(
        lambda o: faker.pydecimal(min_value=2.00, max_value=20.00, left_digits=2, right_digits=2, positive=True)
    )

    @factory.post_generation
    def packages(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if type(extracted) == list:
            # packages_number = random.randint(4,10)
            # A list of groups were passed in, use them
            for package in extracted:
                self.packages.add(package)
