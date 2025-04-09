from django.views import generic
from django.views.generic import TemplateView

from store.models import Product, Category


class HomeView(TemplateView):
    template_name = "store/home.html"


class ProductListView(generic.ListView):
    model = Product


class ProductDetailView(generic.DetailView):
    model = Product


class CategoryListView(generic.ListView):
    model = Category


class CartView(generic.TemplateView):
    template_name = "store/cart.html"
