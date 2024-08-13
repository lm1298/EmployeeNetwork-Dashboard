# myapp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Department(models.Model):
    name = models.CharField(max_length=100)
    manager = models.CharField(max_length=100, blank=True, null=True)
    coordinator = models.CharField(max_length=100, blank=True, null=True)
    dept_chat = models.URLField(max_length=200, blank=True, null=True)
    task = models.TextField(blank=True, null=True)
    dept_email = models.EmailField(max_length=100, blank=True, null=True)
    description = models.TextField()
    key_documents = models.FileField(upload_to='department_documents/', blank=True, null=True)  # Changed to FileField
    goals= models.FileField(upload_to='department_goals/', blank=True, null=True)  # Changed to FileField
    faqs= models.FileField(upload_to='department_faqs/', blank=True, null=True)  # Changed to FileField
    curriculum= models.FileField(upload_to='department_curriculum/', blank=True, null=True)  # Changed to FileField
    def __str__(self):
        return self.name
    
class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # Changed from CharField to ForeignKey
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # Add this line
    
    def __str__(self):
        return f"{self.user.username} - {self.position}"

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateField()
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

class Reminder(models.Model):
    event_title = models.CharField(max_length=255,default="Reminder")
    remind_at = models.DateTimeField()

    def __str__(self):
        return self.event_title
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='events', blank=True, null=True)
    user = models.ManyToManyField(User, related_name='events', blank=True)

    def __str__(self):
        return self.title
    
class Calendar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    events = models.ManyToManyField(Event, related_name='calendar_events', blank=True)
    
class TimeEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    work_hours = models.PositiveIntegerField(default=0)
    work_minutes = models.PositiveIntegerField(default=0)
    summary = models.TextField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(default=now) 
    vacation = models.BooleanField(default=False)  # Field to specify absence
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='time_entries', blank=True, null=True)

    @property
    def hours_to_minutes(self):
        return self.work_hours * 60 + self.work_minutes

    def __str__(self):
        return f"{self.user.username}'s entry on {self.date.date()}"

    @staticmethod
    def total_working_hours(user):
        time_entries = TimeEntry.objects.filter(user=user, vacation=False)
        total_minutes = sum(entry.hours_to_minutes for entry in time_entries)
        return total_minutes / 60  # Convert minutes to hours
