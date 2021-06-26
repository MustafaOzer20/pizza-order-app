# Generated by Django 3.0.3 on 2021-06-26 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0007_auto_20210621_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductsRatings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=200)),
                ('ratings', models.IntegerField()),
                ('userId', models.IntegerField()),
                ('productId', models.IntegerField()),
                ('categoryId', models.IntegerField()),
            ],
        ),
    ]