
# Create your views here.
from rest_framework import generics
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

INDEX_PAGE_TEMPLATE = "products/index.html"

# List all products
class GetProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given product,
        by filtering against a `category` query parameter in the URL.
        """
        queryset = Product.objects.prefetch_related('images','variations').all()
        category_id = self.request.query_params.get('category', None)
        variation_name = self.request.query_params.get('variations', None)
        variation_value = self.request.query_params.get('variation_value', None)

        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
    
        if variation_name and variation_value:
            queryset = queryset.filter(variations__variation_name=variation_name
            , variations__variation_value=variation_value).distinct()

        return queryset

# Retrieve a product
class GetSpecificProductView(generics.RetrieveAPIView):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    

# Retrieve categories
class GetCategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()