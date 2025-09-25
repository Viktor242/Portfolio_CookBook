from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SignUpForm, UserUpdateForm


def signup(request):
    """Регистрация и авто-вход"""
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)   # авто-вход
            return redirect("users:me")
    else:
        form = SignUpForm()
    return render(request, "users/signup.html", {"form": form})


@login_required
def dashboard(request):
    """Личный кабинет"""
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:me")
    else:
        form = UserUpdateForm(instance=request.user)

    # вот тут можно добавить collections (если у тебя они связаны с юзером)
    collections = request.user.collections.all() if hasattr(request.user, "collections") else []

    return render(
        request,
        "users/dashboard.html",
        {"form": form, "collections": collections},
    )