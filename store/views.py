from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic, View
from django.views.generic import TemplateView

from store.forms import CartItemForm
from store.models import Product, Category, CartItem, Cart


class HomeView(TemplateView):
    template_name = "store/home.html"


class ProductListView(generic.ListView):
    model = Product


class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CartItemForm()
        return context


class CategoryListView(generic.ListView):
    model = Category


class CategoryProductListView(generic.ListView):
    model = Product

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Product.objects.filter(category=pk)


class CartListView(generic.ListView):
    template_name = "store/cart_list.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CartItem.objects.filter(cart__user=self.request.user)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            return CartItem.objects.filter(cart__session_key=session_key)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context["cart_items"]
        context["total_order_price"] = sum(item.total_price for item in cart_items)
        return context


class CartItemCreateView(generic.CreateView):
    model = CartItem
    form_class = CartItemForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(
                user=self.request.user
            )
        else:
            if not self.request.session.session_key:
                self.request.session.create()
            cart, created = Cart.objects.get_or_create(
                session_key=self.request.session.session_key
            )

        form.instance.cart = cart
        form.instance.product = Product.objects.get(pk=self.kwargs["product_id"])
        self.object = form.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("store:product-detail", kwargs={"pk": self.object.product.id})


class CustomLoginView(View):
    def get(self, request):
        return render(request, "registration/login.html", {"form": AuthenticationForm()})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            request.session['pre_login_key'] = request.session.session_key
            login(request, form.get_user())
            return redirect("store:home")
        return render(request, "registration/login.html", {"form": form})


class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("store:home")
