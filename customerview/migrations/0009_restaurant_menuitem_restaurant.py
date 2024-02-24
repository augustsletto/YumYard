# Generated by Django 4.2.10 on 2024-02-23 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerview', '0008_delete_menu_delete_restaurant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='menuitem',
            name='restaurant',
            field=models.ManyToManyField(related_name='restaurant', to='customerview.restaurant'),
        ),
    ]