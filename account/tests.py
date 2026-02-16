from django.test import TestCase

# Create your tests here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializers import *  # تأكد من كتابة الاسم الصحيح

@api_view(['POST'])
def register(request):
    data = request.data  # يحصل على البيانات المُرسلة من الـ POST
    user = SingUpSerializers(data=data)  # تمرير البيانات إلى الـ serializer للتحقق منها

    if user.is_valid():  # إذا كانت البيانات صحيحة حسب الشروط في الـ serializer
        if not User.objects.filter(username=data['email']).exists():  # إذا لم يكن هناك مستخدم بنفس الإيميل
            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['email'],  # يتم استخدام الإيميل كاسم مستخدم
                password=make_password(data['password']),  # تشفير كلمة المرور
            )
            return Response(
                {'details': 'Your account registered successfully!'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'details': 'This email already exists!'},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(user.errors)  # في حالة البيانات غير صحيحة يتم إرجاع الأخطاء
