
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from afb_network.forms import EventForm, TimeCardForm
from .models import Department, EmployeeProfile, Announcement, Reminder,  Event, Calendar, TimeEntry
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib import messages


@login_required
def home(request):
    return render(request, 'profile_list.html')

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

def user_calendar(request, user_id):
    employee = get_object_or_404(EmployeeProfile, user__id=user_id)
    user_events = Event.objects.filter(user=employee.user)
    context = {'events': user_events, 'user_id': user_id}
    return render(request, 'calendar.html', context)

def user_timecard(request, user_id):
    employee = get_object_or_404(EmployeeProfile, user__id=user_id)
    time_entries = TimeEntry.objects.filter(employee=employee)
    context = {'time_entries': time_entries}
    return render(request, 'timecard.html', context)

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
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start = request.POST.get('start')
        end = request.POST.get('end')
        if not (title and start and end):
            return JsonResponse({'error': 'Missing title, start, or end'}, status=400)
        event = Event(user=request.user, title=title, start_time=start, end_time=end)
        try:
            event.save()
            return JsonResponse({'id': event.id}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

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

def create_event(request, user_id):
    employee = get_object_or_404(EmployeeProfile, user__id=user_id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.employee = employee
            event.save()
            return redirect('user_calendar', user_id=user_id)
    else:
        form = EventForm()
    context = {'form': form, 'user_id': user_id}
    return render(request, 'calendar.html', context)
    
@login_required
def timecard(request):
    if request.method == 'POST':
        form = TimeCardForm(request.POST)
        if form.is_valid():
            timecard = form.save(commit=False)
            timecard.user = request.user
            timecard.save()
            messages.success(request, 'Timecard submitted successfully.')
            return redirect('timecard_entry')
    else:
        form = TimeCardForm()
    
    # Fetch all timecards
    all_timecards = TimeEntry.objects.all()
    # Fetch only the logged-in user's timecards
    user_timecards = TimeEntry.objects.filter(user=request.user)
    
    return render(request, 'timecard.html', {
        'form': form,
        'user_timecards': user_timecards,
        'all_timecards': all_timecards
    })


@login_required
def edit_timecard(request, timecard_id):
    timecard = get_object_or_404(TimeEntry, id=timecard_id, user=request.user)
    
    if request.method == 'POST':
        form = TimeCardForm(request.POST, instance=timecard)
        if form.is_valid():
            form.save()
            messages.success(request, 'Timecard updated successfully.')
            return redirect('timecard')
    else:
        form = TimeCardForm(instance=timecard)
    
    return render(request, 'edit_timecard.html', {'form': form, 'timecard': timecard})


