from django.contrib.auth import user_logged_in
from django.dispatch import receiver

from store.models import Cart, CartItem


@receiver(user_logged_in)
def merge_carts_on_login(sender, request, user, **kwargs):
    session_key = request.session.get("pre_login_key")
    if not session_key:
        return

    session_cart = Cart.objects.filter(
        session_key=session_key, user=None
    ).first()
    if not session_cart:
        return

    user_cart, created = Cart.objects.get_or_create(user=user)

    for item in session_cart.items.all():
        if not created:
            existing_item = CartItem.objects.filter(
                cart=user_cart, product=item.product
            ).first()
            if existing_item:
                existing_item.quantity += item.quantity
                existing_item.save()
                continue

        CartItem.objects.create(
            cart=user_cart, product=item.product, quantity=item.quantity
        )

    session_cart.delete()
