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
        "get_state",
        "city",
        "quantity",
        "user",
        "price_for_one",
        "price_for_all",
        "image_thumbnail",
    )
    actions = ["finish"]

    def price_for_one(self, obj):
        return obj.product.price

    def price_for_all(self, obj):
        return obj.quantity * obj.product.price

    def city(self, obj):
        return obj.product.city

    def get_state(self, obj):
        return obj.state

    def image_thumbnail(self, obj):
        return mark_safe(
            f'<img src="{obj.product.image.url}" width="150" height="100" />'
        )

    def finish(self, request, queryset):
        for obj in queryset:
            obj.state = "Finished"
            obj.save()

    class StateFilter(admin.SimpleListFilter):
        title = "state"
        parameter_name = "state"

        def lookups(self, request, model_admin):
            return (
                ("In cart", "In cart"),
                ("Bought", "Bought"),
                ("Finished", "Finished"),
            )

        def queryset(self, request, queryset):
            value = self.value()
            if value == "In cart":
                return queryset.filter(state="In cart")
            elif value == "Bought":
                return queryset.filter(state="Bought")
            elif value == "Finished":
                return queryset.filter(state="Finished")

    class CitiFilter(admin.SimpleListFilter):
        title = "city"
        parameter_name = "city"

        def lookups(self, request, model_admin):
            return (
                ("Wroclaw", "Wroclaw"),
                ("Gdansk", "Gdansk"),
                ("Rzeszow", "Rzeszow"),
            )

        def queryset(self, request, queryset):
            value = self.value()
            if value == "Wroclaw":
                return queryset.filter(product__city__shortcut="WRO")
            elif value == "Gdansk":
                return queryset.filter(product__city__shortcut="GDA")
            elif value == "Rzeszow":
                return queryset.filter(product__city__shortcut="RZE")

    list_filter = (StateFilter, CitiFilter)


admin.site.register(Producer)
admin.site.register(Category)
admin.site.register(Computer)
admin.site.register(City)
