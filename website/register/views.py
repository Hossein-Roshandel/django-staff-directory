from django.views import View
from django.shortcuts import render, redirect, resolve_url
from django.views.decorators.http import require_http_methods
from .forms import UserRegisterForm

# Create your views here.


class RegisterUser(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "register/register.html", {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(resolve_url("index"))
        return render(request, "register/register.html", {"form": form})
