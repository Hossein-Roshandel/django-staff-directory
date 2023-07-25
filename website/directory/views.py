from django.shortcuts import render
from django.http import HttpResponse
from django.http.request import HttpRequest
# Create your views here.

def index(request:HttpRequest):   
    return HttpResponse("Hello, world. You're at the staff directory index.")
