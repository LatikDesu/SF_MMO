# Generated by Django 4.2.3 on 2023-07-21 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='users/default_avatar.jpg', null=True, upload_to='users'),
        ),
    ]
