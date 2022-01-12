from django.contrib.admin import AdminSite
from product.views import CartItem


class EventAdminSite(AdminSite):

    site_header = "PGS Store Admin"
    site_title = "PGS Store Admin"
    index_title = "Welcome to PGS Store admin panel"


event_admin_site = EventAdminSite(name="event_admin")
event_admin_site.register(CartItem)
