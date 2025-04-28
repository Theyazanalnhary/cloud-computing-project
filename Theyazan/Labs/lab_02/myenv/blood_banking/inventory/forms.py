# inventory/forms.py

from django import forms
from .models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['blood_type', 'quantity', 'expiration_date']
