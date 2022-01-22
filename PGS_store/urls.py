from django.contrib import admin
from product.admin import small_admin_site

from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from product.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("small-admin/", small_admin_site.urls),
    path("", index, name="home"),
    path("category/<id>/", category),
    path("product/<id>/", product),
    path("cart/", cart, name="cart"),
    path("members/", include("members.urls")),
    path("members/", include("django.contrib.auth.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("cart/add/<int:id>/", cart_add, name="cart_add"),
    path("cart/item_clear/<int:id>/", item_clear, name="item_clear"),
    path("cart/item_increment/<int:id>/", item_increment, name="item_increment"),
    path("cart/item_decrement/<int:id>/", item_decrement, name="item_decrement"),
    path("cart/cart_clear/", cart_clear, name="cart_clear"),
    path("cart/cart-detail/", cart_detail, name="cart_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "PGS Store Admin"
admin.site.site_title = "PGS Store Admin"
admin.site.index_title = "Welcome to PGS Store admin panel"
