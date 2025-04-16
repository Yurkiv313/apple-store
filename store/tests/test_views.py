from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from store.models import Product, Category, CartItem, Cart, Order

User = get_user_model()


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Laptops")
        self.product = Product.objects.create(
            name="MacBook", price=1499.00, category=self.category,
            memory="256 GB", color="Gray", description="Powerful laptop"
        )
        self.user = User.objects.create_user(username="testuser", password="pass123")

    def test_product_list_status(self):
        res = self.client.get(reverse("store:product-list"))
        self.assertEqual(res.status_code, 200)

    def test_product_detail_status(self):
        res = self.client.get(reverse("store:product-detail", args=[self.product.id]))
        self.assertEqual(res.status_code, 200)

    def test_cart_view_empty(self):
        res = self.client.get(reverse("store:cart"))
        self.assertEqual(res.status_code, 200)

    def test_add_to_cart_authenticated(self):
        self.client.force_login(self.user)
        res = self.client.post(
            reverse("store:add-to-cart", args=[self.product.id]),
            data={"quantity": 1}
        )
        self.assertEqual(res.status_code, 302)
        self.assertTrue(CartItem.objects.filter(cart__user=self.user).exists())

    def test_order_creation(self):
        self.client.force_login(self.user)
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)

        res = self.client.post(reverse("store:order-create"))
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Order.objects.filter(user=self.user).exists())
