from django import forms

from package.models import Order


class BulkSendForm(forms.Form):
    delivery_company = forms.ChoiceField(choices=Order.Delivery.choices, required=True)
