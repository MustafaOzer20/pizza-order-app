# Generated by Django 3.0.3 on 2021-06-26 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0011_auto_20210626_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='forRating',
            field=models.CharField(default='0.0', max_length=500, null=True),
        ),
    ]
