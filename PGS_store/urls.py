from django.contrib import admin
from events.admin import event_admin_site

from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from product.views import *

urlpatterns = [
    path("entity-admin/", admin.site.urls),
    path("event-admin/", event_admin_site.urls),
    path("", index, name="home"),
    path("category/<id>/", category),
    path("product/<id>/", product),
    path("cart/", cart, name="cart"),
    path("members/", include("members.urls")),
    path("members/", include("django.contrib.auth.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "PGS Store Admin"
admin.site.site_title = "PGS Store Admin"
admin.site.index_title = "Welcome to PGS Store admin panel"
