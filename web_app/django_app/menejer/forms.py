from django import forms


class FurnitureForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    description = forms.CharField(label='description')
    price = forms.IntegerField(label='price')
    quantity = forms.IntegerField(label='quantity')
    image = forms.CharField(label='image')
