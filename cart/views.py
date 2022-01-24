from django.shortcuts import render, redirect
from product.models import Product
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

    if quantity > Product.objects.get(id=id).quantity - in_cart:
        messages.success(request, (f"Nie możesz dodać tylu produktów do koszyka"))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    cart = Cart(request)
    product = Product.objects.get(id=id)
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
