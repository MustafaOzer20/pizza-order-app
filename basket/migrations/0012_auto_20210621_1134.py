# Generated by Django 3.0.3 on 2021-06-21 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0011_auto_20210617_0955'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basketitem',
            old_name='pizzaId',
            new_name='categoryId',
        ),
        migrations.RenameField(
            model_name='orderpizza',
            old_name='pizzasIds',
            new_name='categoryIds',
        ),
        migrations.AddField(
            model_name='basketitem',
            name='productId',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='orderpizza',
            name='productIds',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
