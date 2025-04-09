from django.urls import path

from store.views import (
    HomeView,
    ProductListView,
    ProductDetailView,
    CategoryListView,
    CartView
)

app_name = "store"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="product-detail"),
    path("category/", CategoryListView.as_view(), name="category-list"),
    path("cart/", CartView.as_view(), name="cart"),
]
