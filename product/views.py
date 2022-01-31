from django.shortcuts import render
from .models import Product, Category
from django.contrib import messages
from django.conf import settings
from cart.models import Cart


def index(request):
    category_object = Category.objects.all()
    context = {"category_object": category_object}
    return render(request, "index.html", context)


def category(request, id):

    category_object_chosen = Category.objects.get(pk=id)
    product_objects = Product.objects.filter(category=category_object_chosen)

    context = {
        "product_objects": "",
        "priceMin": "",
        "priceMax": "",
        "cityWro": "T",
        "cityGda": "T",
        "cityRze": "T",
        "order": "1",
    }
    if request.GET.get("priceMin"):
        minPrice = request.GET["priceMin"]
        product_objects = product_objects.exclude(price__lte=minPrice)
        if minPrice != "0":
            context["priceMin"] = minPrice

    if request.GET.get("priceMax"):
        maxPrice = request.GET["priceMax"]
        if maxPrice != "0":
            context["priceMax"] = maxPrice
            product_objects = product_objects.filter(price__lte=maxPrice)

    cities = []

    if request.GET.get("get"):
        if request.GET.get("cityWro"):
            cities.append("WRO")
            context["cityWro"] = "T"
        else:
            context["cityWro"] = ""

        if request.GET.get("cityGda"):
            cities.append("GDA")
            context["cityGda"] = "T"
        else:
            context["cityGda"] = ""

        if request.GET.get("cityRze"):
            cities.append("RZE")
            context["cityRze"] = "T"
        else:
            context["cityRze"] = ""
    else:
        cities = ["WRO", "GDA", "RZE"]

    product_objects = product_objects.filter(city__shortcut__in=cities)
    product_objects = product_objects.exclude(quantity__lte=0)

    if request.GET.get("order"):
        if request.GET.get("order") == "1":
            product_objects = product_objects.order_by("price")
            context["order"] = 1
        if request.GET.get("order") == "2":
            product_objects = product_objects.order_by("-price")
            context["order"] = 2
        if request.GET.get("order") == "3":
            product_objects = product_objects.order_by("name")
            context["order"] = 3
        if request.GET.get("order") == "4":
            product_objects = product_objects.order_by("-name")
            context["order"] = 4

    context["product_objects"] = product_objects

    return render(request, "category.html", context)


def product(request, id):

    try:
        product_object = Product.objects.get(pk=id)
    except:
        product_object = []

    try:
        in_cart = request.session.get(settings.CART_SESSION_ID)[str(id)]["quantity"]
    except:
        in_cart = 0

    category_object = Category.objects.all()
    context = {
        "product_object": product_object,
        "category_object": category_object,
        "in_cart": in_cart,
    }
    return render(request, "product.html", context)


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
