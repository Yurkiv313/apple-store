from django.urls import path

from store.views import (
    HomeView,
    ProductListView,
    ProductDetailView,
    CategoryListView,
    CartView,
    CategoryProductListView,
)

app_name = "store"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="product-detail"),
    path("category/", CategoryListView.as_view(), name="category-list"),
    path("category/<int:pk>/products/", CategoryProductListView.as_view(), name="category-products"),
    path("cart/", CartView.as_view(), name="cart"),
]
