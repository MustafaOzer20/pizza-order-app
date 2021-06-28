from django.db import models
from django.forms import widgets

# Create your models here.


class CategoryManagment(models.Model):
    kindNames = (
        ('Pizza', ('Pizza')),
       ('Kampanya', ('Kampanya')),
       ('Ekstra', ('Ekstra')),
    )
    name = models.CharField(max_length=200)
    kind = models.CharField(
        max_length=200,
        choices=kindNames,
        default= 'Pizza'
        )

class Pizza(models.Model):

    title = models.CharField(max_length=200)
    contents = models.CharField(max_length=500)
    price = models.FloatField()
    imageUrl = models.TextField()
    category = models.CharField(
        max_length=200,
    )
    salesCount = models.IntegerField(default=0)
    forRating = models.CharField(max_length=500,null=True,default="0.0")


    
    def __str__(self):
        return self.title


class ProductsRatings(models.Model):
    comment = models.CharField(max_length=200)
    ratings = models.IntegerField()
    userId = models.IntegerField()
    productId = models.IntegerField()
    categoryId = models.IntegerField()


