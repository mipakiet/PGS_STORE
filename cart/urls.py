from django.urls import path
from cart.views import *

cart_urlpatterns = [
    path("cart/add/<int:id>/", cart_add, name="cart_add"),
    path("cart/item_clear/<int:id>/", item_clear, name="item_clear"),
    path("cart/cart_clear/", cart_clear, name="cart_clear"),
]
