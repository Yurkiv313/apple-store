from django.urls import path

from store.views import (
    HomeView,
    ProductListView,
    ProductDetailView,
    CategoryListView,
    CartListView,
    CategoryProductListView,
    CartItemCreateView,
    OrderCreateView,
    CartItemDeleteView,
)

app_name = "store"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path(
        "products/<int:pk>",
        ProductDetailView.as_view(),
        name="product-detail",
    ),
    path("category/", CategoryListView.as_view(), name="category-list"),
    path(
        "category/<int:pk>/products/",
        CategoryProductListView.as_view(),
        name="category-products",
    ),
    path("cart/", CartListView.as_view(), name="cart"),
    path(
        "cart/item/<int:pk>/delete/",
        CartItemDeleteView.as_view(),
        name="cartitem-delete",
    ),
    path(
        "add-to-cart/<product_id>/",
        CartItemCreateView.as_view(),
        name="add-to-cart",
    ),
    path("order/create/", OrderCreateView.as_view(), name="order-create"),
]
