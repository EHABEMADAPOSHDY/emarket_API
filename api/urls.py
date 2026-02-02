from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('products/',views.ProductListCreateAPIView.as_view()),
    path('products/info/',views.ProductInfoAPIView.as_view()),
    path('products/<int:product_id>/',views.ProductDetailAPIView.as_view() , name='product-detail'),
    path('users/',views.UserListAPIView.as_view()),
]

router = DefaultRouter()
router.register('orders' ,views.OrderViewSet,)
urlpatterns += router.urls