from django.db import models

# Create your models here.
class Pizza(models.Model):
    categoryNames = (
        ('Cazip Pizzalar', ('Cazip Pizzalar')),
       ('Özel Pizzalar', ('Özel Pizzalar')),
       ('Bol Malzemeli Pizzalar', ('Bol Malzemeli Pizzalar')),
       ('Gurme Pizzalar', ('Gurme Pizzalar')),
    )
    title = models.CharField(max_length=200)
    contents = models.CharField(max_length=500)
    price = models.FloatField()
    imageUrl = models.TextField()
    category = models.CharField(
        max_length=200,
        choices=categoryNames,
        default= 'Cazip Pizzalar'
    )

    def __str__(self):
        return self.title
