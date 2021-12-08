from django.db import models
from django.utils import timezone

# Create your models here.

class products(models.Model):
    kind = models.CharField(max_length=30)  #種類
    products = models.CharField(max_length=30)  #商品
    price = models.IntegerField()   #價格

class shopping_cart2(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)  # 手機號碼
    buy_product = models.TextField()
    buy_quantity = models.TextField()
    total_price = models.IntegerField()
    buy_time = models.DateTimeField(auto_now_add=True)