from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProductList, ProductDetail
from .views import UserRegister
#Urlls for the views in views.py
urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),  # Public listing
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegister.as_view(), name='user-register'),  
]