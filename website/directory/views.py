from functools import reduce
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.decorators.http import require_safe, require_POST
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.db.models import Q
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

@require_POST
def search_staff(request:HttpRequest):
    search_fields = ['fname', 'lname', 'bio', 'email', 'phone']
    search_text = request.POST['search_text']
    if search_text == '' or search_text == None:
        return render(request, 'directory/index.html', {})
    else:
        queries = [Q(**{f'{field}__icontains': search_text}) for field in search_fields]
        combined_query = reduce(lambda x, y: x | y, queries)

        staffs = Staff.objects.filter(combined_query)
        return render(request, 'directory/index.html', {'staffs': staffs, 'query':search_text})
