# Generated by Django 3.0.3 on 2021-06-16 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0004_remove_pizza_gain'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='gain',
            field=models.FloatField(null=True),
        ),
    ]
