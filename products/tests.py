from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Product, CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class ProductAPITestCase(APITestCase):
    
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword'
        )
        # Create a product for testing purposes
        self.product = Product.objects.create(
            name='Test Product',
            description='A test product.',
            price=10.99,
            stock_quantity=100
        )
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
    
    def test_register_user(self):
        url = reverse('user-register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)  # Ensure user was created
    
    def test_token_obtain_pair(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_product_list_public(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure product is listed
    
    def test_create_product_authenticated(self):
        url = reverse('product-create')
        data = {
            'name': 'New Product',
            'description': 'A new product description.',
            'price': 29.99,
            'stock_quantity': 50
        }
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)  # Ensure product was created
    
    def test_create_product_unauthenticated(self):
        url = reverse('product-create')
        data = {
            'name': 'New Product',
            'description': 'A new product description.',
            'price': 29.99,
            'stock_quantity': 50
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_product_detail_authenticated(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)
    
    def test_update_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        data = {
            'name': 'Updated Product',
            'description': 'Updated description.',
            'price': 15.99,
            'stock_quantity': 150
        }
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')
    
    def test_delete_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)  # Ensure product was deleted