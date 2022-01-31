from django.contrib import admin

from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from product.views import *
from cart.urls import cart_urlpatterns

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", index, name="home"),
        path("category/<int:id>/", category, name="category"),
        path("product/<int:id>/", product, name="product"),
        path("cart/", cart, name="cart"),
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + cart_urlpatterns
)

admin.site.site_header = "PGS Store Admin"
admin.site.site_title = "PGS Store Admin"
admin.site.index_title = "Welcome to PGS Store admin panel"
