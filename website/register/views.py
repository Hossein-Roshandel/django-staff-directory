from django.shortcuts import render, redirect, resolve_url
from django.views.decorators.http import require_http_methods
from .forms import UserRegisterForm

# Create your views here.


@require_http_methods(["GET", "POST"])
def register(response):
    form: UserRegisterForm = None
    if response.method == "GET":
        form = UserRegisterForm()

    elif response.method == "POST":
        form = UserRegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect(resolve_url("index"))

    return render(response, "register/register.html", {"form": form})
