from django.contrib import admin
from .models import Products,Cart,Order
# Register your models here.

class Productadmin(admin.ModelAdmin):
    list_display=[
        "userid",
        "productid",
        "productname",
        "category",
        "description",
        "price",
        "images"
    ]

class Cartadmin(admin.ModelAdmin):
    list_display=[
        "userid",
        "productid",
        "qty"
    ]

class Orderadmin(admin.ModelAdmin):
    list_display=[
        "orderid",
        "userid",
        "productid",
        "qty",
    ]

admin.site.register(Products,Productadmin)
admin.site.register(Cart,Cartadmin)
admin.site.register(Order,Orderadmin)