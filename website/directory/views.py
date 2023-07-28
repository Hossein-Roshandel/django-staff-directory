from django.shortcuts import render
from django.http import HttpResponse
from django.http.request import HttpRequest
from .models import Staff
# Create your views here.

def index(request:HttpRequest):

    context = {'staffs': Staff.objects.all()}
    return render(request, 'directory/index.html', context)
