# Generated by Django 4.2.10 on 2024-02-25 21:06

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerview', '0009_restaurant_menuitem_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='featured_image',
            field=cloudinary.models.CloudinaryField(default='placeholder', max_length=255, verbose_name='image'),
        ),
    ]