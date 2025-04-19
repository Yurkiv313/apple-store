from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from store.models import Category, Product

User = get_user_model()


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@example.com"
        )
        self.client.force_login(self.admin_user)

        self.user = User.objects.create_user(
            username="testuser", password="userpass", phone_number="123456789"
        )

        self.category = Category.objects.create(
            name="iPhones", description="Phones"
        )
        self.product = Product.objects.create(
            name="iPhone 15",
            price=999.00,
            category=self.category,
            memory="128 GB",
            battery_capacity="3000",
            screen_size="6.1",
            color="Black",
            description="Latest iPhone",
        )

    def test_user_phone_number_displayed(self):
        url = reverse("admin:store_customuser_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.user.phone_number)

    def test_category_admin_display(self):
        url = reverse("admin:store_category_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.category.name)
        self.assertContains(res, self.category.description)

    def test_product_admin_display(self):
        url = reverse("admin:store_product_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.product.name)
        self.assertContains(res, self.product.price)
        self.assertContains(res, self.category.name)
