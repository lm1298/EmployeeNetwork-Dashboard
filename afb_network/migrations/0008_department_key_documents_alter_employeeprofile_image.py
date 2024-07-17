# Generated by Django 5.0.6 on 2024-07-14 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afb_network', '0007_employeeprofile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='key_documents',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]
