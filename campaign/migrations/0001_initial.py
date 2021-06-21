# Generated by Django 3.0.3 on 2021-06-21 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageUrl', models.URLField()),
                ('title', models.CharField(max_length=300)),
                ('price', models.FloatField()),
                ('category', models.CharField(choices=[('Pizzalar', 'Pizzalar'), ('Makarnalar', 'Makarnalar'), ('Dürümler', 'Dürümler'), ('Özel Fırsatlar', 'Özel Fırsatlar')], default='Pizzalar', max_length=200)),
            ],
        ),
    ]