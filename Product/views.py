from django.shortcuts import render

from django.views.decorators.csrf import csrf_protect
from .models import Product, Category, CartItem
from django.contrib import messages


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
            product_objects = product_objects.order_by("title")
            context["order"] = 3
        if request.GET.get("order") == "4":
            product_objects = product_objects.order_by("-title")
            context["order"] = 4

    context["product_objects"] = product_objects

    return render(request, "list.html", context)


def product(request, id):

    try:
        product_object = Product.objects.get(pk=id)
    except:
        product_object = []

    try:
        in_cart = CartItem.objects.get(
            user=request.user, product=product_object
        ).quantity
    except:
        in_cart = 0

    if request.POST.get("counter"):
        if product_object.quantity >= int(request.POST.get("counter")) + in_cart:
            try:
                cart_object = CartItem.objects.get(
                    user=request.user, product=product_object
                )
                cart_object.quantity += int(request.POST.get("counter"))
                cart_object.save()

            except:
                cart_object = CartItem(
                    product=product_object,
                    user=request.user,
                    quantity=request.POST.get("counter"),
                )
                cart_object.save()
            in_cart += int(request.POST.get("counter"))
            messages.success(
                request,
                (
                    f"Dodano do koszyka {request.POST.get('counter')} {product_object.title}"
                ),
            )
        else:
            messages.success(request, (f"Nie możesz dodać takiej ilości produktu"))

    category_object = Category.objects.all()
    context = {
        "product_object": product_object,
        "category_object": category_object,
        "in_cart": in_cart,
    }
    return render(request, "product.html", context)


def cart(request):

    if request.POST.get("cart_object_id"):
        print(request.POST.get("cart_object_id"))
        CartItem.objects.get(pk=request.POST.get("cart_object_id")).delete()

    try:
        cart_object = CartItem.objects.filter(user=request.user)
    except:
        cart_object = []

    price_for_everything = 0

    objects = []
    for cart in cart_object:
        product = Product.objects.get(id=cart.product.id)
        objects.append((product, cart, product.price * cart.quantity))
        price_for_everything += product.price * cart.quantity

    context = {"objects": objects, "price_for_everything": price_for_everything}

    return render(request, "cart.html", context)
