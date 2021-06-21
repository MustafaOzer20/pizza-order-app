from django.db import models

# Create your models here.
class Extra(models.Model):
    categoryNames = (
        ('Dürümler', ('Dürümler')),
       ('Atıştırmalık & Sos', ('Atıştırmalık & Sos')),
       ('Makarnalar', ('Makarnalar')),
       ('Tatlılar', ('Tatlılar')),
       ('İçecekler', ('İçecekler')),
    )
    imageUrl = models.URLField()
    title = models.CharField(max_length=300)
    contents = models.CharField(max_length=300, null=True)
    price = models.FloatField()
    category = models.CharField(
        max_length=200,
        choices=categoryNames,
        default= 'Pizzalar'
    )


    def __str__(self):
        return self.title