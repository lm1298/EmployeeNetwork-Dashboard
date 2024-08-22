#admin.py
from django.contrib import admin

from .forms import EmployeeProfileForm
from .models import  Announcement, Department, EmployeeProfile, Reminder, Calendar, Event, TimeEntry, ChatMessage

class EmployeeProfileAdmin(admin.ModelAdmin):
    form = EmployeeProfileForm

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'video')

admin.site.register(Event)
admin.site.register(EmployeeProfile)
admin.site.register(Announcement)
admin.site.register(Reminder)
admin.site.register(Department)  # Register the Department model
admin.site.register(TimeEntry)
admin.site.register(Calendar)
admin.site.register(ChatMessage)


