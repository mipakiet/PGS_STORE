from django import forms
from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Zalogowałeś się"))
            return redirect("home")
        else:
            messages.success(request, ("Błedne hasło bądź login"))
            return redirect("login_user")
    else:
        return render(request, "login_user.html", {})


def logout_user(request):
    messages.success(request, ("Wylogowałeś się"))
    logout(request)
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Zarejestowałeś się"))
            return redirect("home")
    else:
        form = UserCreationForm()

    context = {"form": form}

    return render(request, "register_user.html", context)
