# Generated by Django 5.0.6 on 2024-07-11 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afb_network', '0006_employeeprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
