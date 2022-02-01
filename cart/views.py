from django.shortcuts import render, redirect
from product.models import Product, CartItem
from .models import Cart
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages


def cart(request):

    price_for_everything = 0
    if request.session.get(settings.CART_SESSION_ID):
        for key, item in request.session.get(settings.CART_SESSION_ID).items():
            product = Product.objects.get(id=item["product_id"])
            if product.quantity < item["quantity"]:

                cart_obj = Cart(request)
                cart_obj.decrement(
                    product=product, quantity=item["product_id"] - product.quantity
                )
                messages.success(
                    request, (f"Produkt który miałeś w koszyku został kupiony  :(")
                )

            price_for_everything += int(item["quantity"]) * int(product.price)

    context = {"price_for_everything": price_for_everything}

    return render(request, "cart.html", context)


def cart_add(request, id, quan=1):
    if request.GET.get("counter"):
        quantity = int(request.GET["counter"])
    else:
        quantity = quan

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

    context = {
        "name": name,
        "address": address,
        "cart": request.session.get(settings.CART_SESSION_ID),
    }

    price_for_all = 0

    if request.GET.get("company_name") and request.GET.get("nip"):
        context["company_name"] = request.GET.get("company_name")
        context["nip"] = request.GET.get("nip")
        for key, item in request.session.get(settings.CART_SESSION_ID).items():
            product = Product.objects.get(id=item["product_id"])
            product.quantity -= item["quantity"]
            product.save()
            price_for_all += item["quantity"] * product.price

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

    else:
        for key, item in request.session.get(settings.CART_SESSION_ID).items():
            product = Product.objects.get(id=item["product_id"])
            product.quantity -= item["quantity"]
            product.save()
            price_for_all += item["quantity"] * product.price

            cart_item = CartItem(
                employee_name=name,
                address=address,
                product=Product.objects.get(id=item["product_id"]),
                quantity=item["quantity"],
                price=item["price"],
            )
            cart_item.save()

    context["price_for_all"] = price_for_all

    cart = Cart(request)
    cart.clear()

    return render(request, "summary.html", context)


def summary(request):
    return render(request, "summary.html")
