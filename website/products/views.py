
# Create your views here.
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

INDEX_PAGE_TEMPLATE = "products/index.html"

# List all products or create a new one
class GetProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given product,
        by filtering against a `category` query parameter in the URL.
        """
        queryset = Product.objects.all()
        category = self.request.query_params.get('category')
        print("HELLO", category)
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset

# Retrieve, update, or delete a product
class GetSpecificProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    