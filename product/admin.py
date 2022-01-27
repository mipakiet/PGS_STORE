from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from datetime import date
from django.contrib import messages


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


class CategoryFilter(admin.SimpleListFilter):
    title = "category"
    parameter_name = "category"

    def lookups(self, request, model_admin):
        queryset = Category.objects.all()
        categories = []
        for obj in queryset:
            categories.append((obj.id, obj.name))
        print(categories)
        return categories

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(product__category=value)
        else:
            return queryset


class ReleasedFilter(admin.SimpleListFilter):
    title = "released"
    parameter_name = "released"

    def lookups(self, request, model_admin):
        return ((True, "Yes"), (False, "No"))

    def queryset(self, request, queryset):

        if not queryset:
            return queryset
        value = self.value()
        if value is not None:
            return queryset.filter(released=value)
        else:
            return queryset


class BillFilter(admin.SimpleListFilter):
    title = "bill"
    parameter_name = "bill"

    def lookups(self, request, model_admin):
        return ((True, "Yes"), (False, "No"))

    def queryset(self, request, queryset):

        if not queryset:
            return queryset
        value = self.value()
        if value is not None:
            return queryset.filter(bill=value)
        else:
            return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "image_thumbnail",
        "name",
        "city",
        "quantity",
        "price",
        "price_for_all",
    )
    readonly_fields = ["image_thumbnail"]
    actions = ["add_1", "subtrack_1"]
    list_filter = ("category", CityFilter)

    def price_for_all(self, obj):
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
        "image_thumbnail",
        "order_date",
        "bill",
        "released",
        "released_date",
        "city",
        "employee_name",
        "address",
        "nip",
        "company_name",
        "quantity",
        "price",
        "price_for_all",
    )
    list_filter = (CityFilter, CategoryFilter, ReleasedFilter, BillFilter)
    actions = ["release", "bill", "cancel"]

    def price_for_all(self, obj):
        return obj.quantity * obj.price

    def city(self, obj):
        return obj.product.city

    def image_thumbnail(self, obj):
        return mark_safe(
            f'<img src="{obj.product.image.url}" width="150" height="100" />'
        )

    def release(self, request, queryset):
        for obj in queryset:
            obj.released_date = date.today()
            obj.released = True
            obj.save()

    def bill(self, request, queryset):
        for obj in queryset:
            obj.bill = True
            obj.save()

    def cancel(self, request, queryset):
        for obj in queryset:
            if obj.released or obj.bill:
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"{obj.product.name} ma wystawiona fakture albo jest wydany. Nie możesz go usunąć",
                )
            else:
                obj.product.quantity += obj.quantity
                obj.product.save()
                obj.delete()


admin.site.register(Category)
admin.site.register(City)
