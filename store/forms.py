from django import forms

from store.models import CartItem


class CartItemForm(forms.ModelForm):

    class Meta:
        model = CartItem
        fields = ["quantity", ]
