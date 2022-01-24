from django.urls import path
from cart.views import *

cart_urlpatterns = [
    path("cart/add/<int:id>/", cart_add, name="cart_add"),
    path("cart/item_clear/<int:id>/", item_clear, name="item_clear"),
    path("cart/item_increment/<int:id>/", item_increment, name="item_increment"),
    path("cart/item_decrement/<int:id>/", item_decrement, name="item_decrement"),
    path("cart/cart_clear/", cart_clear, name="cart_clear"),
    path("cart/cart-detail/", cart_detail, name="cart_detail"),
]
