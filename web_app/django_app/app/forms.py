from django import forms

class PaymentForm(forms.Form):
    amount = forms.CharField(label='Amount', max_length=100)
    payment_status = forms.CharField(label='Payment Status', max_length=100)
    payment_type = forms.CharField(label='Payment Type', max_length=100)


class CargoForm(forms.Form):
    delivery_address = forms.CharField(label='Delivery Address', max_length=100)
    delivery_status = forms.CharField(label='Delivery Status', max_length=100)
