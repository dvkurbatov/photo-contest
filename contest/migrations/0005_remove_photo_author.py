# Generated by Django 3.0.5 on 2020-04-17 00:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0004_remove_photo_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='author',
        ),
    ]
