from rest_framework.decorators import api_view ,permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework import status
from .models import *
from .serializers import ProductSerializers
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg
@api_view(['GET'])
def get_all_product(request):
    filterset = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    conut = filterset.qs.count()
    resPage = 12
    paginator = PageNumberPagination()
    paginator.page_size = resPage
    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = ProductSerializers(queryset, many=True)
    return Response({'products': serializer.data , 'count':conut , 'resPage':resPage})
@api_view(['GET'])
def get_by_id_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    serializer = ProductSerializers(product, many=False)
    return Response({'products': serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    data = request.data
    serializer=ProductSerializers(data=data)
    if serializer.is_valid():
        product= Product.objects.create(**data,user=request.user)
        res = ProductSerializers(product, many=False)
        return Response({'products': res.data})
    else:
        return Response(serializer.errors)
   
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_product(request,pk):
    product = get_object_or_404(Product, id=pk)
    if product.user != request.user:#لتاكد انه صحاب المنتج من اجل التعديل او الحزف
        return Response({"error":"Sorey you can not update this product"}, status=status.HTTP_403_FORBIDDEN)
    product.name=request.data['name']
    product.description=request.data['description']
    product.price=request.data['price']
    product.brand=request.data['brand']
    product.ratings=request.data['ratings']
    product.stock=request.data['stock']
    product.save()
    serializer = ProductSerializers(product,many=False)
    return Response({'products': serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated , IsAdminUser])
def delet_product(request,pk):
    product = get_object_or_404(Product, id=pk)
    if product.user != request.user:
        return Response({"error":"Sorey you can not update this product"}, status=status.HTTP_403_FORBIDDEN)
    product.delete()
    return Response({'products':"Delete action is doue"},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_review(request, pk):
    user = request.user
    data = request.data
    product = get_object_or_404(Product, id=pk)
    existing_review = product.reviews.filter(user=user)
    if data['rating'] <= 0 or data['rating'] > 5:
        return Response({"error": 'Please select a rating between 1 and 5 only'}, status=status.HTTP_400_BAD_REQUEST)
    elif existing_review.exists():
        updated_data = {'rating': data['rating'], 'comment': data['comment']}
        existing_review.update(**updated_data)
        rating = product.reviews.aggregate(avg_ratings=Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()
        return Response({'details': 'Product review updated'})
    else:
        Review.objects.create(
            user=user,
            product=product,
            rating=data['rating'],
            comment=data['comment'],
        )
        rating = product.reviews.aggregate(avg_ratings=Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()
        return Response({'details': 'Product review created'})
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_review(request,pk):
    user = request.user
    product = get_object_or_404(Product,id=pk)
    review = product.reviews.filter(user=user)
    if review.exists():
        review.delete()
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        if rating['avg_ratings'] is None:
            rating['avg_ratings'] = 0
            product.ratings = rating['avg_ratings']
            product.save()
            return Response({'deleils':"Product review deleted"})
    else:
        return Response ({'error':'Review not found'},status=status.HTTP_404_NOT_FOUND)