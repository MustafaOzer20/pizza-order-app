from django.db import models
import datetime

SIZE_CHOICES = (
    ("1", "Küçük Boy"),
    ("2", "Orta Boy"),
    ("3", "Büyük Boy"),
)

# Create your models here.
class BasketItem(models.Model):
    #userId = models.IntegerField(null=True)
    productId = models.IntegerField(null=True)
    piece = models.IntegerField(default=1)
    size = models.CharField(max_length = 100, choices=SIZE_CHOICES, default="Orta Boy")
    categoryId = models.IntegerField() # 1-pizzas, 2-campaign 3-extra
    user = models.ForeignKey("auth.User",on_delete=models.CASCADE,null=True)




class OrderPizza(models.Model):
    basketId = models.IntegerField()
    #userId = models.IntegerField()
    productIds =  models.CharField(max_length = 150,null=True)
    size = models.CharField(max_length=200)
    piece = models.CharField(max_length=200)
    sum_price = models.FloatField()
    adress = models.TextField(max_length=300)
    phone_number = models.CharField(max_length=11)
    user_note = models.CharField(max_length=200, null=True, blank=True)
    payment_method = models.CharField(max_length=200)
    status = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    categoryIds =  models.CharField(max_length = 150)
    user = models.ForeignKey("auth.User",on_delete=models.CASCADE,null=True)

    class Meta:
        ordering = ['-created_date']
    