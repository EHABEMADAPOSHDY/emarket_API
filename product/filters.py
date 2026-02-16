import django_filters
from .models import *

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    keyword = django_filters.CharFilter(field_name="name",lookup_expr="icontains")
    minPrice = django_filters.NumberFilter(field_name="price" or 0, lookup_expr="gte" )# لا يقل عن
    maxPrice = django_filters.NumberFilter(field_name="price" or 100000, lookup_expr="lte" )#لا يزيد عن
    class Meta:
        model = Product
        #fields = ['name', 'category']
        fields = ('name', 'category','keyword', 'minPrice' , 'maxPrice')