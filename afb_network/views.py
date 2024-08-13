
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from afb_network.forms import EventForm, TimeEntryForm
from .models import Department, EmployeeProfile, Announcement, Reminder,  Event, Calendar, TimeEntry
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib import messages
import json


@login_required
def home(request):
    return render(request, 'profile_list.html')

def profile_page(request):
    departments = Department.objects.all()
    profiles = EmployeeProfile.objects.select_related('user', 'department').all()
    announcements = Announcement.objects.all()
    reminders = Reminder.objects.all()
    groups = Group.objects.all()
    timecard= TimeEntry.objects.all()
    events= Event.objects.all()
    total_hours= TimeEntry.total_working_hours(user=request.user)
    context = {
        'departments': departments,
        'profiles': profiles,
        'announcements': announcements,
        'reminders': reminders,
        'groups': groups,
        'timecard': timecard,
        'events': events,
        'total_hours': total_hours
    }
    return render(request, 'profile_list.html', context)

def talk(request, user_id):
    
    user_profile = get_object_or_404(EmployeeProfile, user__id=user_id)
    
    return HttpResponse("Talk page for: " + user_profile.user.username)

def user_calendar(request, user_id):
    employee = get_object_or_404(EmployeeProfile, user__id=user_id)
    user_events = Event.objects.filter(user=employee.user)
    context = {'events': user_events, 'user_id': user_id}
    return render(request, 'calendar.html', context)


@receiver(post_save, sender=User)
def create_user_calendar(sender, instance, created, **kwargs):
    if created:
        Calendar.objects.create(user=instance)

@login_required
def fetch_events(request):
    events = Event.objects.filter(user=request.user).values('id', 'title', 'start_time', 'end_time')
    event_list = list(events)
    return JsonResponse(event_list, safe=False)

@login_required
@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'errors': 'Invalid JSON data'}, status=400)

        form = EventForm(data)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            event_data = {
                'id': event.id,
                'title': event.title,
                'start': event.start_time.isoformat(),
                'end': event.end_time.isoformat(),
            }
            return JsonResponse({'status': 'success', 'event': event_data})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'invalid request'}, status=400)

@login_required
def event_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        employee = EmployeeProfile.objects.get(user=user)
        events = Event.objects.filter(employee=employee)
        event_list = [{
            'title': event.title,
            'start': event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'end': event.end_time.strftime("%Y-%m-%dT%H:%M:%S") if event.end_time else None,
        } for event in events]
        return JsonResponse(event_list, safe=False)
    except EmployeeProfile.DoesNotExist:
        return JsonResponse({'error': 'Employee profile not found'}, status=404)


@login_required
@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'errors': 'Invalid JSON data'}, status=400)

        form = EventForm(data)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            event_data = {
                'id': event.id,
                'title': event.title,
                'start': event.start_time.isoformat(),
                'end': event.end_time.isoformat(),
            }
            return JsonResponse({'status': 'success', 'event': event_data})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'invalid request'}, status=400)

@login_required
def user_timecard(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            time_entry = form.save(commit=False)
            time_entry.user = user  # Assign the User instance
            time_entry.save()
            messages.success(request, 'Timecard submitted successfully.')
            return redirect('user_timecard', user_id=user_id)
    else:
        form = TimeEntryForm()

    employee = get_object_or_404(EmployeeProfile, user=user )
    time_entries = TimeEntry.objects.filter(employee=employee).order_by('-date')
    total_hours = sum(entry.hours_to_minutes for entry in time_entries) / 60
    users = User.objects.all()

    context = {
        'time_entries': time_entries,
        'total_hours': total_hours,
        'user_id': user_id,
        'form': form, 
        'user': user

    }
    return render(request, 'timecard.html', context)


@login_required
def add_time_entry(request, user_id):
    user = get_object_or_404(User, id=user_id)
    employee = get_object_or_404(EmployeeProfile, user=user)
    
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            time_entry = form.save(commit=False)
            time_entry.user = user  # Assign the User instance
            time_entry.save()
            messages.success(request, 'Timecard submitted successfully.')
            return redirect('add_time_entry', user_id=user_id)
    else:
        form = TimeEntryForm()
    return render(request, 'timecard.html', {'form': form, 'user': employee})


@login_required
def edit_timecard(request, timecard_id):
    timecard = get_object_or_404(TimeEntry, id=timecard_id, user=request.user)
    
    if request.method == 'POST':
        form = TimeEntryForm(request.POST, instance=timecard)
        if form.is_valid():
            form.save()
            messages.success(request, 'Timecard updated successfully.')
            return redirect('user_timecard', user_id=request.user.id)  # Pass user_id instead of user
    else:
        form = TimeEntryForm(instance=timecard)
    
    return render(request, 'edit_timecard.html', {'form': form, 'timecard': timecard})


def profile_list(request):
    users = User.objects.all()
    user_timecards = {}
    for user in users:
        last_timecard = TimeEntry.objects.filter(user=user).order_by('-date').first()
        user_timecards[user.id] = last_timecard
    return render(request, 'profile_list.html', {'users': users, 'user_timecards': user_timecards})