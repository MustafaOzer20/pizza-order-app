# Generated by Django 3.0.3 on 2021-06-16 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='gain',
            field=models.IntegerField(null=True),
        ),
    ]
