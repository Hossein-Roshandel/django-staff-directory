from django.urls import path
from .views import GetProductListView, GetSpecificProductView, GetCategoryListView

urlpatterns = [
    path('', GetProductListView.as_view(), name='product-list-create'),
    path('<int:pk>/', GetSpecificProductView.as_view(), name='product-detail'),
    path('category/', GetCategoryListView.as_view(), name='category-list'),
]