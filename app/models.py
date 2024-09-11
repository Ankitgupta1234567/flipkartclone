from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class CustomerManager(models.Manager):
    def mobile_list(self):
        return self.filter(category__exact="mobile")
    def electronics_list(self):
        return self.filter(category__exact="electrnoics")
    def pricerange(self,r1,r2):
        return self.filter(price__range=(r1,r2))
    

class Products(models.Model):
    userid=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    productid=models.IntegerField(primary_key=True)
    productname=models.CharField(max_length=100)
    type=(
        ("mobile", "Mobile"),
        ("electronics", "Electronics"),
        ("fashion", "Fashion"),
        ("babyproduct", "Baby Product"),
    )
    category=models.CharField(max_length=100,choices=type)
    description=models.TextField()
    price=models.FloatField()
    images=models.ImageField(upload_to="photos")
    objects=models.Manager()
    productmanager=CustomerManager()

class Cart(models.Model):
    userid=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    productid=models.ForeignKey(Products,on_delete=models.CASCADE,null=True)
    qty=models.PositiveIntegerField(default=0)

class Order(models.Model):
    orderid=models.IntegerField(primary_key=True)
    userid=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    productid=models.ForeignKey(Products,on_delete=models.CASCADE,null=True)
    qty=models.PositiveIntegerField(default=0)
