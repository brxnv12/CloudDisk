from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RoyxatdanOtishForm, KirishForm
from .models import User


def royxatdan_otish(request):
    if request.user.is_authenticated:
        return redirect("storage:dashboard")
    form = RoyxatdanOtishForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            name=form.cleaned_data["name"],
            password=form.cleaned_data["password"],
            email=form.cleaned_data.get("email", ""),
        )
        login(request, user)
        return redirect("storage:dashboard")
    return render(request, "accounts/royxatdan_otish.html", {"form": form})


def kirish(request):
    if request.user.is_authenticated:
        return redirect("storage:dashboard")
    form = KirishForm(request.POST or None)
    error = None
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user:
            login(request, user)
            return redirect(request.GET.get("next", "storage:dashboard"))
        else:
            error = "Username yoki parol noto'g'ri"
    return render(request, "accounts/kirish.html", {"form": form, "error": error})


def chiqish(request):
    logout(request)
    return redirect("accounts:kirish")
