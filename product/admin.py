from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "quantity", "price", "add_up", "image_thumbnail")
    readonly_fields = ["image_thumbnail"]
    actions = ["add_1", "subtrack_1"]

    def add_up(self, obj):
        return obj.price * obj.quantity

    def subtrack_1(self, request, queryset):
        for obj in queryset:
            obj.quantity = obj.quantity - 1
            obj.save()

    def add_1(self, request, queryset):
        for obj in queryset:
            obj.quantity = obj.quantity + 1
            obj.save()

    def image_thumbnail(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="150" height="100" />')


@admin.register(CartItem)
class CartItem(admin.ModelAdmin):
    list_display = (
        "product",
        "quantity",
        "user",
        "price_for_one",
        "price_for_all",
        "image_thumbnail",
    )
    actions = ["close"]

    def price_for_one(self, obj):
        return obj.product.price

    def price_for_all(self, obj):
        return obj.quantity * obj.product.price

    def image_thumbnail(self, obj):
        return mark_safe(
            f'<img src="{obj.product.image.url}" width="150" height="100" />'
        )

    def close(self, request, queryset):
        for obj in queryset:
            obj.product.quantity -= obj.quantity
            obj.product.save()
            obj.delete()


admin.site.register(Producer)
admin.site.register(Category)
admin.site.register(Computer)
admin.site.register(City)
