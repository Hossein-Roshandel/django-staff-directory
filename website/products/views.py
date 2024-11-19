
# Create your views here.
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

INDEX_PAGE_TEMPLATE = "products/index.html"

# List all products or create a new one
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Retrieve, update, or delete a product
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer