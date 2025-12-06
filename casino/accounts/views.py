from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password != password2:
            messages.error(request, "Паролі не співпадають!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Користувач уже існує!")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        user.save()

        messages.success(request, "Реєстрація успішна! Увійдіть у систему.")
        return redirect("login")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")   # головна сторінка
        else:
            messages.error(request, "Невірний логін або пароль!")
            return redirect("login")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")
