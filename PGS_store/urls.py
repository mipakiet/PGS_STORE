from django.contrib import admin

from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from product.views import *
from cart.urls import cart_urlpatterns

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

handler400 = "product.views.handler400"
handler403 = "product.views.handler403"
handler404 = "product.views.handler404"
handler500 = "product.views.handler500"

urlpatterns = (
    [
        path(
            "favicon.ico",
            RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
        ),
        path("admin/", admin.site.urls),
        path("", index, name="home"),
        path("category/<int:id>/", category, name="category"),
        path("product/<int:id>/", product, name="product"),
        path("__debug__/", include("debug_toolbar.urls")),
        path("regulamin/", statute, name="statute"),
        path("search", search, name="search"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + cart_urlpatterns
)

admin.site.site_header = "PGS Store Admin"
admin.site.site_title = "PGS Store Admin"
admin.site.index_title = "Welcome to PGS Store admin panel"
