import django_filters
from api.models import *
from rest_framework import filters


class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.all()

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name' : ['exact' , 'contains'],
            'price': ['exact', 'lt', 'gt', 'range'],
            }
        
class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at': ['lt', 'gt', 'exact'],
        }
