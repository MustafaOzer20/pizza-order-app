from django.db import models

# Create your models here.
class Campaign(models.Model):
    imageUrl = models.URLField()
    title = models.CharField(max_length=300)
    price = models.FloatField()
    category = models.CharField(
        max_length=200,
    )


    def __str__(self):
        return self.title