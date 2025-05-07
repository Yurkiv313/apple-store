from django.test import TestCase
from store.forms import CartItemForm, CustomUserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CartItemFormTests(TestCase):
    def test_valid_quantity(self):
        form = CartItemForm(data={"quantity": 3})
        self.assertTrue(form.is_valid())

    def test_invalid_quantity_zero(self):
        form = CartItemForm(data={"quantity": 0})
        self.assertFalse(form.is_valid())


class CustomUserCreationFormTests(TestCase):
    def test_valid_user_creation(self):
        form_data = {
            "username": "testuser",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "123456789",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "testuser")

    def test_passwords_do_not_match(self):
        form_data = {
            "username": "testuser",
            "password1": "pass1",
            "password2": "pass2",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "123456789",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
