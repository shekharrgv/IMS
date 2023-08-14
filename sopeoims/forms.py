# sopeonow/forms.py
from django import forms
from .models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['IName','ICost', 'IQuantity', 'ISellingprice']

class Order_received(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['IName','ICost', 'IQuantity', 'ISellingprice']


class InventoryItemEditForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['IName', 'ICost', 'IQuantity', 'ISellingprice']
       
from django import forms
from .models import InventoryItem

class InventoryItemSellForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['IQuantitysold']
        
class InventoryItemBuyForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['IQuantity','IIN','Order']

class BuyForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['Order']

from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['IName', 'ICost', 'Order', 'Date', 'Status']


# forms.py
from django import forms

class OrderForm(forms.Form):
    Order = forms.IntegerField(label='Order Quantity', required=True)

