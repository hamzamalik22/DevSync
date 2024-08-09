# Generated by Django 5.0 on 2024-08-09 15:53

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dm8tng2j0/image/upload/v1723218301/lltf6bhysrpkaslzw6dt.jpg', max_length=255, verbose_name='image'),
        ),
    ]