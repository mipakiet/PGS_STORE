import os.path
from django.shortcuts import render, redirect
from product.models import Product, CartItem
from product.views import handler404
from .models import Cart
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.options import get_content_type_for_model


def check_cart_with_db(request):
    if request.session.get(settings.CART_SESSION_ID):
        cart_copy = request.session.get(settings.CART_SESSION_ID).copy()
        for key, item in cart_copy.items():
            if Product.objects.filter(id=item["product_id"]).exists():
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
                    return False
            else:
                cart_obj = Cart(request)
                cart_obj.remove_from_id(product_id=item["product_id"])
                messages.success(
                    request,
                    (
                        f"Produkt {item['name']} który miałeś w koszyku został usunięty  :("
                    ),
                )
                return False
        return True


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
    check_cart_with_db(request)
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

    if not Product.objects.filter(id=id).exists():
        messages.success(request, f"Produkt został usunięty :(")
        return redirect("home")

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

    # check that the data is valid
    if not (
        request.GET.get("firstName")
        and request.GET.get("secondName")
        and request.GET.get("login")
        and request.GET.get("statute")
        and request.GET.get("address")
    ):
        return handler404(request)

    if request.GET.get("company"):
        if not (request.GET.get("company_name") and request.GET.get("nip")):
            return handler404(request)

    # check cart with database
    if not check_cart_with_db(request):
        return redirect("cart")

    # check if cart is not empty
    if len(request.session.get(settings.CART_SESSION_ID)) == 0:
        messages.success(request, ("Nie masz nic w koszyku"))
        return redirect("cart")

    # assign variables
    name = request.GET.get("firstName") + " " + request.GET.get("secondName")
    address = request.GET.get("address")
    login = request.GET.get("login")
    context = {
        "name": name,
        "login": str(login),
        "address": address,
        "cart": request.session.get(settings.CART_SESSION_ID),
    }

    if request.GET.get("company"):
        context["company_name"] = request.GET.get("company_name")
        context["address"] = request.GET.get("address")

    price_for_all = 0

    if CartItem.objects.filter().exists():
        order_id = CartItem.objects.all().last().order_id + 1
    else:
        order_id = 0

    # send mail
    if not send_email(request):
        return redirect("cart")

    # buy
    for key, item in request.session.get(settings.CART_SESSION_ID).items():
        product = Product.objects.get(id=item["product_id"])
        product.quantity -= item["quantity"]
        product.save()
        price_for_all += item["quantity"] * product.price
        cart_item = CartItem(
            order_id=order_id,
            employee_name=name,
            login=login,
            address=address,
            product=Product.objects.get(id=item["product_id"]),
            quantity=item["quantity"],
            price=item["price"],
        )
        if request.GET.get("company"):
            cart_item.company_name = (request.GET.get("company_name"),)
            cart_item.nip = (request.GET.get("nip"),)

        cart_item.save()

        # add log
        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=get_content_type_for_model(cart_item).pk,
            object_id=cart_item.pk,
            object_repr=str(cart_item),
            action_flag=CHANGE,
            change_message="Added.",
        )

    context["price_for_all"] = price_for_all

    # clear cart
    Cart(request).clear()

    return render(request, "summary.html", context)


def send_email(request):

    price_for_all = 0
    for key, item in request.session.get(settings.CART_SESSION_ID).items():
        price_for_all += (
            item["quantity"] * Product.objects.get(id=item["product_id"]).price
        )

    context = {
        "cart": request.session.get(settings.CART_SESSION_ID),
        "price_for_all": price_for_all,
        "name": request.GET.get("firstName"),
        "surname": request.GET.get("secondName"),
        "login": request.GET.get("login"),
    }

    if request.GET.get("company"):
        context["company_name"] = request.GET.get("company_name")
        context["address"] = request.GET.get("address")
        context["nip"] = request.GET.get("nip")
        context["company"] = True

    html_content = render_to_string("mail_summary.html", context)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(
        "Podsumowanie zamówienia",
        text_content,
        to=[f"{request.GET.get('login')}@pgs-soft.com"],
    )
    msg.attach_alternative(html_content, "text/html")

    with open("static/pgsLogo.png", mode="rb") as f:
        image = MIMEImage(f.read())
        msg.attach(image)
        image.add_header("Content-ID", "<pgsLogo>")

    for key, item in request.session.get(settings.CART_SESSION_ID).items():
        with open(item["image"][1:], mode="rb") as f:
            image = MIMEImage(f.read())
            msg.attach(image)
            image.add_header("Content-ID", f"<{item['product_id']}>")
    try:
        msg.send()
        return True
    except:
        messages.success(request, ("Nastąpił błąd z wysyłaniem maila"))
        return False
