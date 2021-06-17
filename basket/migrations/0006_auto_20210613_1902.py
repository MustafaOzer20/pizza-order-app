# Generated by Django 3.0.3 on 2021-06-13 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0005_orderpizza_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderpizza',
            name='payment_method',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='orderpizza',
            name='user_note',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='orderpizza',
            name='status',
            field=models.IntegerField(),
        ),
    ]
