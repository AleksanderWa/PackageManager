from django.test import TestCase

from package.forms import BulkSendForm
from package.models import Order


class BulkSendFormTest(TestCase):
    def test_validate_delivery_choices(self):
        form = BulkSendForm({"delivery_company": "blabla"})
        self.assertEqual(form.is_valid(), False)

        form = BulkSendForm({"delivery_company": Order.Delivery.DPD})
        self.assertEqual(form.is_valid(), True)
