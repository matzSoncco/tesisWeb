# Generated by Django 5.0.6 on 2024-07-27 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('almacen', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duration',
            name='duration',
            field=models.IntegerField(),
        ),
    ]
