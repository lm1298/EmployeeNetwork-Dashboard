# Generated by Django 5.0.2 on 2024-07-26 02:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afb_network', '0004_alter_event_employee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='timeentry',
            name='employee',
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='calendar',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='afb_network.calendar'),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='event',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='afb_network.event'),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='time_card',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='afb_network.timeentry'),
        ),
    ]
