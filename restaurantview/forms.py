from django import forms
from django.forms import ModelForm
from customerview.models import MenuItem


# Create a menu form
class MenuForm(ModelForm):
    class Meta:
        model = MenuItem
        fields = (
            'name',
            'description',
            'image',
            'price',
            'category',
            'restaurant',
            )
        labels = {
            'name': 'Item Name',
            'description': 'Description',
            'image': 'Upload Image',
            'price': 'Add Price',
            'category': 'Choose Category',
            'restaurant': 'Choose Restaurant',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control'}),
            'image': forms.FileInput(attrs={
                'class': 'form-control', 'id': 'customFile'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control'}),
            'category': forms.SelectMultiple(attrs={
                'class': 'form-control'}),
            'restaurant': forms.SelectMultiple(attrs={
                'class': 'form-control'}),
        }