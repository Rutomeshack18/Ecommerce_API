from django.shortcuts import render
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics
from .models import Product
from .serializers import UserSerializer
from .models import CustomUser
from .permissions import IsAuthenticatedOrReadOnly

#User registerview to allow users to register
class UserRegister(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
#A product list view that allow users to list and create the products
#Implemented a custom permission that allows users to GET the product but requires authentication to POST
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        category = self.request.query_params.get('category', None)
        price_min = self.request.query_params.get('price_min', None)
        price_max = self.request.query_params.get('price_max', None)
        in_stock = self.request.query_params.get('in_stock', None)

        if name:
            queryset = queryset.filter(name__icontains=name)  # Partial match for name
        if category:
            queryset = queryset.filter(category__name__icontains=category)  # Assuming category is a ForeignKey
        if price_min is not None:
            queryset = queryset.filter(price__gte=price_min)
        if price_max is not None:
            queryset = queryset.filter(price__lte=price_max)
        if in_stock is not None:
            queryset = queryset.filter(stock_quantity__gt=0)

        return queryset

#ProductDetail view that allowa users to see detail of a product update or delete if authenticated
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

