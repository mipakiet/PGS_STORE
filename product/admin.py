from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from datetime import date
from django.contrib import messages
from django.contrib.admin.helpers import ActionForm
from django import forms
from simple_history.admin import SimpleHistoryAdmin


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
                return queryset.filter(product__city=value)
            elif isinstance(queryset[0], Product):
                return queryset.filter(city=value)
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


class BilledFilter(admin.SimpleListFilter):
    title = "billed"
    parameter_name = "billed"

    def lookups(self, request, model_admin):
        return ((True, "Yes"), (False, "No"))

    def queryset(self, request, queryset):

        if not queryset:
            return queryset
        value = self.value()
        if value is not None:
            return queryset.filter(billed=value)
        else:
            return queryset


class AddSubQuantityForm(ActionForm):
    quantity = forms.IntegerField(required=False)


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["spec"].required = False

    class Meta:
        model = Product
        fields = "__all__"


@admin.register(Product)
class ProductAdmin(SimpleHistoryAdmin):
    form = ProductForm
    list_display = (
        "image_thumbnail",
        "name",
        "city",
        "quantity",
        "price",
        "price_for_all",
    )
    readonly_fields = ["image_thumbnail"]
    actions = ["add_or_subtract", "delete"]
    action_form = AddSubQuantityForm
    list_filter = ("category", CityFilter)
    history_list_display = ["status"]
    list_per_page = 10

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["quantity"]
        else:
            return []

    def price_for_all(self, obj):
        return obj.price * obj.quantity

    def add_or_subtract(self, request, queryset):
        if not request.POST["quantity"]:
            messages.add_message(request, messages.ERROR, f"Podaj ilosc")
            return
        for obj in queryset:
            if obj.quantity + int(request.POST["quantity"]) < 0:
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"'{obj.name}' ilość produktu nie może być ujemna",
                )
            else:
                obj.quantity += int(request.POST["quantity"])
                obj.save()

    def delete(self, request, queryset):
        for obj in queryset:
            obj.delete()

    def get_actions(self, request):
        actions = super().get_actions(request)

        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def image_thumbnail(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="150" height="100" />')


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = "__all__"

    def clean(self):
        super(CartItemForm, self).clean()

        # get data
        product_quantity = self.cleaned_data.get("product").quantity
        quantity = self.cleaned_data.get("quantity")

        # check is object editing
        if self.instance.pk is None:
            if product_quantity - quantity < 0:
                self._errors["quantity"] = self.error_class(
                    ["Product don't have that much quantity"]
                )
        else:
            if product_quantity - (quantity - self.instance.quantity) < 0:
                self._errors["quantity"] = self.error_class(
                    ["Product don't have that much quantity"]
                )
        return self.cleaned_data


@admin.register(CartItem)
class CartItemAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "order_id",
        "product_name",
        "image_thumbnail",
        "order_date",
        "billed",
        "released",
        "released_date",
        "city",
        "employee_name",
        "login",
        "address",
        "nip",
        "company_name",
        "quantity",
        "price",
        "price_for_all",
    )
    list_filter = (CityFilter, CategoryFilter, ReleasedFilter, BilledFilter)
    actions = ["release", "bill", "cancel"]
    history_list_display = ["released", "billed"]
    exclude = ["order_id"]
    readonly_fields = ["released", "billed", "released_date"]
    list_per_page = 10
    form = CartItemForm

    # displayed name
    def product_name(self, obj):
        return obj.product.name

    def price_for_all(self, obj):
        return obj.quantity * obj.price

    def city(self, obj):
        return obj.product.city

    def image_thumbnail(self, obj):
        return mark_safe(
            f'<img src="{obj.product.image.url}" width="150" height="100" />'
        )

    # actions
    def release(self, request, queryset):
        for obj in queryset:
            obj.released_date = date.today()
            obj.released = True
            obj.save()

    def bill(self, request, queryset):
        for obj in queryset:
            obj.billed = True
            obj.save()

    def cancel(self, request, queryset):
        for obj in queryset:
            if obj.released or obj.billed:
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"{obj.product.name} ma wystawiona fakture albo jest wydany. Nie możesz go usunąć",
                )
            else:
                obj.product.quantity += obj.quantity
                obj.product.save()
                obj.delete()

    # change behavior
    def save_model(self, request, obj, form, change):

        if change:
            cart_item_to_change = CartItem.objects.get(id=obj.id)
            difference = obj.quantity - cart_item_to_change.quantity

            if obj.product.quantity - difference < 0:
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"{obj.product.name} nie ma wystarczającej ilości",
                )
                return
            else:
                product = obj.product
                product.quantity -= difference
                product.save()

        else:
            obj.order_id = CartItem.objects.last().order_id + 1
            if obj.product.quantity - obj.quantity < 0:
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"{obj.product.name} nie ma wystarczającej ilości",
                )
                return
            else:
                product = obj.product
                product.quantity -= obj.quantity
                product.save()

        obj.user = request.user
        super(CartItemAdmin, self).save_model(request, obj, form, change)

        # def delete_model(self, request, obj):
        #     product = obj.product
        #     product.quantity += obj.quantity
        #     product.save()
        # super().delete_model(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_staff:
            if request.user.is_superuser:
                return True
            else:
                return False

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_staff:
            if request.user.is_superuser:
                return []
            else:
                return ["released", "billed", "released_date"]


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Category)
