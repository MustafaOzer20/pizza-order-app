# Generated by Django 3.0.3 on 2021-06-26 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0009_pizza_forrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='salesCount',
            field=models.IntegerField(null=True),
        ),
    ]
