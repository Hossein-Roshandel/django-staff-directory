from django.urls import path
from .admin import directory_admin_site

from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path('portal/',directory_admin_site.urls),
]