from django.db import models
from django import forms
from cloudinary.models import CloudinaryField



class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = ('#')

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    image = CloudinaryField('image', default='placeholder')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')
    featured_image = CloudinaryField('image', default='placeholder')
    restaurant = models.ManyToManyField(
        'Restaurant', related_name='restaurant')

    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    street = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    zip_code = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)


    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'
