from django.shortcuts import render, redirect
from product.models import Product
from .models import Cart


def cart_add(request, id):
    if request.GET.get("counter"):
        quantity = request.GET["counter"]
    else:
        quantity = -1
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product, quantity=quantity)
    return redirect("home")


# def cart_add(request, id, quan):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.add(product=product, quantity=quan)
#     return redirect("home")


def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


def cart_detail(request):
    return render(request, "cart/cart_detail.html")
