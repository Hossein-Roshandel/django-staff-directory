from django.urls import path
from .views import GetProductListView, GetSpecificProductView

urlpatterns = [
    path('', GetProductListView.as_view(), name='product-list-create'),
    path('<int:pk>/', GetSpecificProductView.as_view(), name='product-detail'),
]