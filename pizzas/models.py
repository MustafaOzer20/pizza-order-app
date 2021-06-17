from django.db import models
from django.db.models.base import Model

# Create your models here.
class Pizza(models.Model):
    title = models.CharField(max_length=200)
    contents = models.CharField(max_length=500)
    price = models.FloatField()
    imageUrl = models.TextField()
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.title
