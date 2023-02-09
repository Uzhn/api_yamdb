# Generated by Django 3.2 on 2023-02-09 11:18

from django.db import migrations, models
import reviews.models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(validators=[reviews.models.validate_year], verbose_name='Год создания'),
        ),
    ]