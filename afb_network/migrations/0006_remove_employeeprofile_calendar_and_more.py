# Generated by Django 5.0.2 on 2024-07-26 16:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afb_network', '0005_remove_event_employee_remove_timeentry_employee_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeeprofile',
            name='calendar',
        ),
        migrations.RemoveField(
            model_name='employeeprofile',
            name='event',
        ),
        migrations.RemoveField(
            model_name='employeeprofile',
            name='time_card',
        ),
        migrations.RemoveField(
            model_name='event',
            name='user',
        ),
        migrations.AddField(
            model_name='event',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='afb_network.employeeprofile'),
        ),
    ]
