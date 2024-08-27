# Generated by Django 5.1 on 2024-08-27 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('H', 'Home'), ('O', 'Office'), ('OT', 'Other')], max_length=12),
        ),
    ]
