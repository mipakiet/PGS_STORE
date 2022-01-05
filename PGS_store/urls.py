from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from Product.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="home"),
    path('category/<id>/', category),
    path('product/<id>/', product),
    path('cart/', cart, name="cart"),
    path('members/', include('members.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('__debug__/', include('debug_toolbar.urls')),

]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
