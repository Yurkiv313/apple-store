import logging

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import transaction
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import generic, View
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe

from store.forms import CartItemForm, CustomUserCreationForm
from store.models import Product, Category, CartItem, Cart, Order, CustomUser
from store.services.token_service import account_activation_token


class HomeView(TemplateView):
    template_name = "store/home.html"


class ProductListView(generic.ListView):
    model = Product

    def get_queryset(self):
        return Product.objects.select_related("category")


class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.select_related("category")

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
        return Product.objects.select_related("category").filter(category=pk)


class CartListView(generic.ListView):
    template_name = "store/cart_list.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CartItem.objects.select_related(
                "product", "product__category"
            ).filter(cart__user=self.request.user)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            return CartItem.objects.select_related(
                "product", "product__category"
            ).filter(cart__session_key=session_key)

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

        product = Product.objects.get(pk=self.kwargs["product_id"])

        exist_item = CartItem.objects.filter(cart=cart, product=product).first()
        if exist_item:
            exist_item.quantity += form.cleaned_data["quantity"]
            exist_item.save()
            return redirect(self.get_success_url())

        form.instance.cart = cart
        form.instance.product = product
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("store:product-detail", kwargs={"pk": self.kwargs["product_id"]})


class CartItemDeleteView(generic.DeleteView):
    model = CartItem
    success_url = reverse_lazy("store:cart")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.quantity > 1:
            self.object.quantity -= 1
            self.object.save()
            return redirect(self.success_url)

        return super().post(request, *args, **kwargs)


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    fields = []
    login_url = "/login/"
    template_name = "store/order_confirm_page.html"
    success_url = reverse_lazy("store:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("store:cart")
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        CartItem.objects.filter(cart__user=self.request.user).delete()
        messages.success(
            self.request,
            mark_safe(
                "🤖 Дякую за замовлення! Наші дрони зараз зайняті важливою місією (ви знаєте якою...)😎🇺🇦<br>"
                "Але не хвилюйтесь — у мене є... альтернативні способи доставки 🛸... Швидкість — гарантована!!!"
            )
        )

        return super().form_valid(form)


class CustomLoginView(View):
    def get(self, request):
        next_url = request.GET.get("next", "/")
        return render(request, "registration/login.html", {
            "form": AuthenticationForm(),
            "next": next_url
        })

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        next_url = request.POST.get("next", "/")
        if form.is_valid():
            request.session['pre_login_key'] = request.session.session_key
            login(request, form.get_user())
            return redirect(next_url)
        return render(request, "registration/login.html", {
            "form": form,
            "next": next_url
        })


class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("store:home")


class SignUpGenericView(generic.CreateView):
    model = CustomUser
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    @transaction.atomic
    def form_valid(self, form):
        try:
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(self.request)
            mail_subject = "Activate your account."
            message = render_to_string(
                "registration/emails/acc_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.content_subtype = "html"
            email.send()
        except Exception as e:
            logging.error(f"Error sending email: {e}")

            return render(self.request, "registration/signup.html", {"form": form})

        return render(self.request, "registration/email_confirmation_sent.html")


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            # login(request, user)
            messages.success(
                request,
                "🤖 Thank you for confirming your email. You can now login to your account.",
            )
            return redirect("login")
        else:
            return render(request, "registration/activation_invalid.html")
