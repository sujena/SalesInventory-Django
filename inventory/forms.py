from django import forms
from .models import Inventory, Offers


class StockSearchForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['category', 'item_name', 'item_code']



