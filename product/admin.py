from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django.contrib.admin import AdminSite


class CityFilter(admin.SimpleListFilter):
    title = "city"
    parameter_name = "city"

    def lookups(self, request, model_admin):
        return (("WRO", "Wroclaw"), ("GDA", "Gdansk"), ("RZE", "Rzeszow"))

    def queryset(self, request, queryset):

        if not queryset:
            return queryset
        value = self.value()
        if value:
            if isinstance(queryset[0], CartItem):
                return queryset.filter(product__city__shortcut=value)
            elif isinstance(queryset[0], Product):
                return queryset.filter(city__shortcut=value)
        else:
            return queryset


class StateFilter(admin.SimpleListFilter):
    title = "state"
    parameter_name = "state"

    def lookups(self, request, model_admin):
        return (("In cart", "In cart"), ("Bought", "Bought"), ("Finished", "Finished"))

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(state=value)
        else:
            return queryset


class CategoryFilter(admin.SimpleListFilter):
    title = "category"
    parameter_name = "category"

    def lookups(self, request, model_admin):
        queryset = Category.objects.all()
        categories = []
        for obj in queryset:
            categories.append((obj.id, obj.name))
        return categories

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(product__category=value)
        else:
            return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "city", "quantity", "price", "add_up", "image_thumbnail")
    readonly_fields = ["image_thumbnail"]
    actions = ["add_1", "subtrack_1"]
    list_filter = ("category", CityFilter)

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
class CartItemAdmin(admin.ModelAdmin):
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
    list_filter = (StateFilter, CityFilter, CategoryFilter)

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


admin.site.register(Category)
admin.site.register(Computer)
admin.site.register(City)


class SmallAdminSite(AdminSite):
    site_header = "PGS Admin"
    site_title = "PGS Admin Portal"
    index_title = "Welcome to PGS Admin Portal"


small_admin_site = SmallAdminSite(name="small_admin")
small_admin_site.register(Product, ProductAdmin)
small_admin_site.register(CartItem, CartItemAdmin)
