from django.shortcuts import render, redirect
from product.models import Product, CartItem
from .models import Cart
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages


def cart_add(request, id):
    if request.GET.get("counter"):
        quantity = int(request.GET["counter"])
    else:
        quantity = 1

    try:
        in_cart = int(
            request.session.get(settings.CART_SESSION_ID)[str(id)]["quantity"]
        )
    except:
        in_cart = 0

    product = Product.objects.get(id=id)

    if quantity > product.quantity - in_cart:
        messages.success(request, (f"Nie możesz dodać tylu produktów do koszyka"))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    messages.success(request, (f"Dodano {quantity} {product.name} do koszyka"))

    cart = Cart(request)
    cart.add(product=product, quantity=quantity)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


def buy(request):

    if (
        not request.GET.get("firstName")
        or not request.GET.get("secondName")
        or not request.GET.get("address")
    ):
        messages.success(request, ("błędne dane do zakupu"))
        return redirect("cart")

    name = request.GET.get("firstName") + " " + request.GET.get("secondName")
    address = request.GET.get("address")
    if request.GET.get("company_name") and request.GET.get("nip"):
        for key, item in request.session.get(settings.CART_SESSION_ID).items():
            product = Product.objects.get(id=item["product_id"])
            product.quantity -= item["quantity"]
            product.save()

            cart_item = CartItem(
                employee_name=name,
                address=address,
                company_name=request.GET.get("company_name"),
                nip=request.GET.get("nip"),
                product=Product.objects.get(id=item["product_id"]),
                quantity=item["quantity"],
                price=item["price"],
            )
            cart_item.save()

            cart = Cart(request)
            cart.clear()
    else:
        for key, item in request.session.get(settings.CART_SESSION_ID).items():
            product = Product.objects.get(id=item["product_id"])
            product.quantity -= item["quantity"]
            product.save()

            cart_item = CartItem(
                employee_name=name,
                address=address,
                product=Product.objects.get(id=item["product_id"]),
                quantity=item["quantity"],
                price=item["price"],
            )
            cart_item.save()

            cart = Cart(request)
            cart.clear()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
