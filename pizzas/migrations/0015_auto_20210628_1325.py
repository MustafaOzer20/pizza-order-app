# Generated by Django 3.0.3 on 2021-06-28 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0014_auto_20210627_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='category',
            field=models.CharField(max_length=200),
        ),
    ]
