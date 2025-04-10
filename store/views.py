from django.views import generic
from django.views.generic import TemplateView

from store.models import Product, Category


class HomeView(TemplateView):
    template_name = "store/home.html"


class ProductListView(generic.ListView):
    model = Product


class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = "product"


class CategoryListView(generic.ListView):
    model = Category


class CategoryProductListView(generic.ListView):
    model = Product

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Product.objects.filter(category=pk)


class CartView(generic.TemplateView):
    template_name = "store/cart.html"
