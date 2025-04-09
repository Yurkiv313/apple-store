from django.contrib.auth.models import AbstractUser
from django.db import models

from apple_store import settings


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    memory = models.CharField(max_length=30, blank=True)
    battery_capacity = models.CharField(max_length=30, blank=True)
    screen_size = models.CharField(max_length=30, blank=True)
    color = models.CharField(max_length=30, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="product_images/", default="photo.png", blank=True)

    def __str__(self):
        return f"{self.name}, {self.category}, {self.color}, {self.price}$"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        if self.user:
            return f"Cart (User: {self.user.username})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name}, {self.quantity}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}, {self.created_at.strftime('%Y-%m-%d')}"
