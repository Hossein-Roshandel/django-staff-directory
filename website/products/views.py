
# Create your views here.
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

INDEX_PAGE_TEMPLATE = "products/index.html"

# List all products or create a new one
class GetProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Retrieve, update, or delete a product
class GetSpecificProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer