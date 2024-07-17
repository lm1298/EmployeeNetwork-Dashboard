#admin.py
from django.contrib import admin

from .forms import EmployeeProfileForm
from .models import  Announcement, Department, EmployeeProfile, Reminder, TimeCard

class EmployeeProfileAdmin(admin.ModelAdmin):
    form = EmployeeProfileForm

admin.site.register(EmployeeProfile)
admin.site.register(Announcement)
admin.site.register(Reminder)
admin.site.register(TimeCard)
admin.site.register(Department)  # Register the Department model
