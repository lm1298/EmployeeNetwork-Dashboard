# myapp/models.py
from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
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

    def __str__(self):
        return self.title

class Reminder(models.Model):
    event_title = models.CharField(max_length=255,default="Reminder")
    remind_at = models.DateTimeField()

    def __str__(self):
        return self.event_title

class TimeCard(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_time = models.DurationField()

class Calendar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    events = models.ManyToManyField('Event')
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


