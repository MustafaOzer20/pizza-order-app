# Generated by Django 3.0.3 on 2021-06-29 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0013_auto_20210629_0857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basketitem',
            name='userId',
        ),
        migrations.RemoveField(
            model_name='orderpizza',
            name='userId',
        ),
    ]
