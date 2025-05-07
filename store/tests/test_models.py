from django.test import TestCase
from django.contrib.auth import get_user_model

from store.models import Category, Product, Cart, CartItem, Order

User = get_user_model()


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            phone_number="123456789",
        )
        self.category = Category.objects.create(name="iPhones")
        self.product = Product.objects.create(
            name="iPhone 15",
            price=1299.99,
            category=self.category,
            memory="128 GB",
            battery_capacity="3274 mAh",
            screen_size="6.1 inch",
            color="Black",
            description="The best iPhone",
        )

    def test_user_str(self):
        self.assertEqual(str(self.user), self.user.username)

    def test_category_str(self):
        self.assertEqual(str(self.category), "iPhones")

    def test_product_str(self):
        expected = (
            f"{self.product.name}, "
            f"{self.product.category}, "
            f"{self.product.color}, "
            f"{self.product.price}$"
        )
        self.assertEqual(str(self.product), expected)

    def test_cart_str(self):
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(str(cart), f"Cart (User: {self.user.username})")

    def test_cartitem_total_price(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(
            cart=cart, product=self.product, quantity=2
        )
        self.assertEqual(item.total_price, self.product.price * 2)

    def test_cartitem_str(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(
            cart=cart, product=self.product, quantity=3
        )
        self.assertEqual(str(item), f"{self.product.name}, {item.quantity}")

    def test_order_str(self):
        order = Order.objects.create(user=self.user)
        expected = (
            f"{self.user.username}, {order.created_at.strftime('%Y-%m-%d')}"
        )
        self.assertEqual(str(order), expected)
