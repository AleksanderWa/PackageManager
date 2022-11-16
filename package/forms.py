from django import forms

from package.models import Order


class BulkSendForm(forms.Form):
    # DELIVERY_CHOICES = (
    #     (1, "DPD"),
    #     (2, "Fedex"),
    #     (3, "UPS"),
    # )
    delivery_company = forms.ChoiceField(choices=Order.Delivery.choices, required=True)
