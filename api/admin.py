from django.contrib import admin
from api.models import *
from .models import *
# Register your models here.
admin.site.register(User)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]

admin.site.register(Order , OrderAdmin)
