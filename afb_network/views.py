
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Department, EmployeeProfile, Announcement, Reminder, TimeCard
from django.contrib.auth.models import Group

@login_required
def home(request):
    return render(request, 'afb_base.html')

def profile_page(request):
    departments = Department.objects.all()
    profiles = EmployeeProfile.objects.select_related('user', 'department').all()
    announcements = Announcement.objects.all()
    reminders = Reminder.objects.all()
    groups = Group.objects.all()
    context = {
        'departments': departments,
        'profiles': profiles,
        'announcements': announcements,
        'reminders': reminders,
        'groups': groups,
    }
    return render(request, 'profile_list.html', context)

def talk(request, user_id):
    # Assuming you have a UserProfile model linked to your User model
    user_profile = get_object_or_404(EmployeeProfile, user__id=user_id)
    # Implement your logic here
    return HttpResponse("Talk page for: " + user_profile.user.username)

def calendar(request, user_id):
    user_profile = get_object_or_404(EmployeeProfile, user__id=user_id)
    # Implement your logic here
    return HttpResponse("Calendar page for: " + user_profile.user.username)

def time_card(request, user_id):
    user_profile = get_object_or_404(EmployeeProfile, user__id=user_id)
    # Implement your logic here
    return HttpResponse("Time Card page for: " + user_profile.user.username)