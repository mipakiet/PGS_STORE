from django.urls import path
from . import views

urlpatterns = [
    path("logout_user", views.logout_user, name="logout_user"),
    path("login_user", views.login_user, name="login_user"),
    path("register_user", views.register_user, name="register_user"),
]
