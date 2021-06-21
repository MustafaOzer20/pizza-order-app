from django.db import models

# Create your models here.
class Campaign(models.Model):
    categoryNames = (
        ('Pizzalar', ('Pizzalar')),
       ('Makarnalar', ('Makarnalar')),
       ('Dürümler', ('Dürümler')),
       ('Özel Fırsatlar', ('Özel Fırsatlar')),
    )
    imageUrl = models.URLField()
    title = models.CharField(max_length=300)
    price = models.FloatField()
    category = models.CharField(
        max_length=200,
        choices=categoryNames,
        default= 'Pizzalar'
    )


    def __str__(self):
        return self.title