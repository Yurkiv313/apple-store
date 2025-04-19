from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from store.models import CartItem

User = get_user_model()


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = [
            "quantity",
        ]

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return quantity


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email address")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "phone_number",
            "email",
        )


class ProductNameSearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False, label="")
