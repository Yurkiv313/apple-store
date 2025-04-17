from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from store.models import CustomUser, Category, Product, Cart, CartItem, Order


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("phone_number",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("phone_number",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "phone_number",
                    )
                },
            ),
        )
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
        "category",
        "memory",
        "battery_capacity",
        "screen_size",
        "color",
        "description",
        "image",
    ]

    search_fields = ["category__name"]
    ordering = ["price"]


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
