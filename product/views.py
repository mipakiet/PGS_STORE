from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.db.models.functions import Cast


def index(request):
    category_object = Category.objects.all()
    context = {"category_object": category_object}
    if settings.DEBUG:
        context["version"] = settings.VERSION
    return render(request, "index.html", context)


def category(request, id):
    try:
        category_object_chosen = Category.objects.get(pk=id)
    except:
        return handler404(request)

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

    product_objects = product_objects.filter(city__in=cities)
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

    paginator = Paginator(product_objects, 15)

    page = request.GET.get("page")
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context["page_obj"] = page_obj

    return render(request, "category.html", context)


def product(request, id):
    try:
        product_object = Product.objects.get(pk=id)
    except:
        return handler404(request)

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


def search(request):
    context = {
        "product_objects": "",
        "priceMin": "",
        "priceMax": "",
        "cityWro": "T",
        "cityGda": "T",
        "cityRze": "T",
        "order": "1",
    }

    product_objects = Product.objects.all()

    if request.GET.get("look_for"):
        key_word = request.GET["look_for"]
        product_objects = product_objects.filter(
            Q(name__contains=key_word) | Q(description__contains=key_word)
        )
        context["look_for"] = key_word

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

    product_objects = product_objects.filter(city__in=cities)
    product_objects = product_objects.exclude(quantity__lte=0)
    context["amount_of_products"] = len(product_objects)

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

    paginator = Paginator(product_objects, 15)

    if request.GET.get("page"):
        page = request.GET["page"]
    else:
        page = 1

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context["page_obj"] = page_obj

    return render(request, "search.html", context)


def statute(request):
    return render(request, "statute.html")


def handler400(request, *args, **argv):
    context = {"errorcode": "400"}
    return render(request, "error.html", context=context, status=400)


def handler403(request, *args, **argv):
    context = {"errorcode": "403"}
    return render(request, "error.html", context=context, status=403)


def handler404(request, *args, **argv):
    context = {"errorcode": "404"}
    return render(request, "error.html", context=context, status=404)


def handler500(request, *args, **argv):
    context = {"errorcode": "500"}
    return render(request, "error.html", context=context, status=500)
