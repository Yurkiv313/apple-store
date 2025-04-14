from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from store.models import CartItem

User = get_user_model()


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ["quantity", ]


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
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "style": "max-width: 100%;"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "style": "max-width: 100%;"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "style": "max-width: 100%;"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "style": "max-width: 100%;"}),
        }


class ProductNameSearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False, label="")