# Generated by Django 3.0.3 on 2021-06-26 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0010_pizza_salescount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='salesCount',
            field=models.IntegerField(),
        ),
    ]
