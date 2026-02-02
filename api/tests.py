from django.urls import reverse
from api.models import *
from rest_framework.test import APITestCase
from rest_framework.routers import DefaultRouter
from rest_framework import status

class ProductAPITeatCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin' , password='adminpass')
        self.normal_user = User.objects.create_user(username='user' , password='adminpass')
        self.prodoct = Product.objects.create(
            name = 'Test Product',
            description = 'Test Description',
            price = 9.99,
            stock = 10
        )
        self.url = reverse('product-detail' , kwargs={'product_id':self.prodoct.pk})

    def test_get_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code , 200)
        self.assertEqual(response.data['name'], self.prodoct.name)

    def test_unauthorized_update_product(self):
        product = Product.objects.create(name="Test Product")  # منتج تجريبي
        url = reverse('product-detail', args=[product.id])     # مش product-list
        data = {'name': 'Updated Product'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_unauthorized_delete_product(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)
    def test_only_admins_can_delete_product(self):
        self.client.login(username = 'user' , password = '1234')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code , status.HTTP_403_FORBIDDEN) 
        self.assertTrue(Product.objects.filter(pk=self.prodoct.pk).exists())
        
# from django.test import TestCase
# from .models import *
# from django.urls import reverse
# from rest_framework import status
# class UserOrderTestCase(TestCase):
#     def setUp(self):
#         user1 = User.objects.create_user(username='user1' , password='test')
#         user2 = User.objects.create_user(username='user2' , password='test')
#         Order.objects.create(user=user1)
#         Order.objects.create(user=user1)
#         Order.objects.create(user=user2)
#         Order.objects.create(user=user2)
#     def test_user_order_endpoint_retieves_only_authenticated_user_orders(self):
#         user = User.objects.get(username = 'user1')
#         self.client.force_login(user)
#         response = self.client.get(reverse('user_orders'))

#         assert response.status_code == status.HTTP_200_OK
#         orders = response.json()
#         self.assertTrue(all(order['user'] == user.id for order in orders))
#     def test_user_order_list_unauthenticated(self):
#         response = self.client.get(reverse('user_orders'))
#         self.assertEqual(response.status_code , status.HTTP_404_NOT_FOUND)






        