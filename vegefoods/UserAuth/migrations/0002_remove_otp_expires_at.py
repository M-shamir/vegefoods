# Generated by Django 5.1 on 2024-08-20 03:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserAuth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp',
            name='expires_at',
        ),
    ]
