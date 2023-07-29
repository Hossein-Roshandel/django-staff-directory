from django.shortcuts import render
from django.views.generic import DetailView
from django.views.decorators.http import require_safe
from django.http import HttpResponse
from django.http.request import HttpRequest
from .models import Staff
# Create your views here.

@require_safe
def index(request:HttpRequest):

    context = {'staffs': Staff.objects.all()}
    return render(request, 'directory/index.html', context)

class StaffDetailView(DetailView):
    
    model = Staff
    fields = '__all__'
    template_name = 'directory/staff_detail.html'
