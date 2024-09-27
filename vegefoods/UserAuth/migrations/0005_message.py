# Generated by Django 5.1 on 2024-09-27 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAuth', '0004_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=14)),
                ('subject', models.CharField(max_length=10)),
                ('message', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('solved', 'Solved')], max_length=20)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
