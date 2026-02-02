from django.db.models import Max
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import api_view , parser_classes
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated ,
    IsAdminUser ,
    AllowAny
    )
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination , LimitOffsetPagination
from .filters import *
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class ProductListCreateAPIView(generics.ListCreateAPIView):
    throttle_scope = 'products'
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializers 
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend ,
        filters.SearchFilter , 
        filters.OrderingFilter ,
        InStockFilterBackend ,
        ]
    search_fields = ['name' , 'description']
    ordering_fields =['name' , 'price' , 'stock']
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
           self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    @method_decorator(cache_page(60 * 15 , key_prefix='product_list'))
    @method_decorator(vary_on_headers('Authorization'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
    
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    lookup_url_kwarg = 'product_id'
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT' , 'PATCH' , 'DELETE']:
            self.pagination_class = [IsAdminUser]
        return super().get_permissions()

class OrderViewSet(viewsets.ModelViewSet):
    throttle_scope = 'orders'
    queryset = Order.objects.prefetch_related('items')
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [
        DjangoFilterBackend
    ]
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return OrderCreateSerializers
        return super().get_serializer_class()
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user = self.request.user)
        return qs
    @action(detail=False,
            methods=['get'],
            url_path='user-orders',
            permission_classes = [IsAuthenticated]
            )
    def user_order(self , request):
        orders = self.get_queryset().filter(user=request.user)
        serializer  = self.get_serializer(orders , many = True)
        return Response (serializer.data)


# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items')
#     serializer_class = OrderSerializers
    

# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items')
#     serializer_class = OrderSerializers
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)

class ProductInfoAPIView(APIView):
    def get(self , request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
        "products":products , 
        "count":len(products),
        "max_price":products.aggregate(max_price = Max('price'))['max_price']
    })
        return Response (serializer.data)

class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = Userserializers
    pagination_class = None
    