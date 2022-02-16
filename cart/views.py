from django.shortcuts import render, redirect
from product.models import Product, CartItem
from product.views import handler404
from .models import Cart
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages


def check_cart_with_db(request):
    if request.session.get(settings.CART_SESSION_ID):
        cart_copy = request.session.get(settings.CART_SESSION_ID).copy()
        for key, item in cart_copy.items():
            product = Product.objects.get(id=item["product_id"])
            if product.quantity < item["quantity"]:

                cart_obj = Cart(request)
                cart_obj.decrement(
                    product=product, quantity=item["quantity"] - product.quantity
                )
                messages.success(
                    request,
                    (
                        f"Produkt {product.name} który miałeś w koszyku został kupiony  :("
                    ),
                )


def get_cart_price(request):

    price_for_everything = 0
    if request.session.get(settings.CART_SESSION_ID):
        for key, item in request.session.get(settings.CART_SESSION_ID).items():
            price_for_everything += (
                Product.objects.get(id=item["product_id"]).price * item["quantity"]
            )
    return price_for_everything


def cart(request):

    check_cart_with_db(request)
    price_for_everything = get_cart_price(request)

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

    if not (
        request.GET.get("firstName")
        and request.GET.get("secondName")
        and request.GET.get("email")
        and request.GET.get("statute")
    ):
        return handler404(request)

    if request.GET.get("company"):
        if not (
            request.GET.get("company_name")
            and request.GET.get("address")
            and request.GET.get("nip")
        ):
            return handler404(request)

    name = request.GET.get("firstName") + " " + request.GET.get("secondName")
    address = request.GET.get("address")
    email = request.GET.get("email")

    context = {
        "name": name,
        "email": str(email),
        "address": address,
        "cart": request.session.get(settings.CART_SESSION_ID),
    }

    check_cart_with_db(request)

    if len(request.session.get(settings.CART_SESSION_ID)) == 0:
        messages.success(request, ("Nie masz nic w koszyku"))
        return redirect("cart")

    price_for_all = 0

    if request.GET.get("company"):
        context["company_name"] = request.GET.get("company_name")
        context["address"] = request.GET.get("address")
        context["nip"] = request.GET.get("nip")
        for key, item in request.session.get(settings.CART_SESSION_ID).items():
            product = Product.objects.get(id=item["product_id"])
            product.quantity -= item["quantity"]
            product.save()
            price_for_all += item["quantity"] * product.price

            cart_item = CartItem(
                employee_name=name,
                email=email,
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
                email=email,
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
