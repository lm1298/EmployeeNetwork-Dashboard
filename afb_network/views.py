
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Department, EmployeeProfile, Announcement, Reminder, TimeCard, Event, Calendar
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

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

def user_calendar(request, user_id):
    user = get_object_or_404(User, id=user_id)
    calendar = get_object_or_404(Calendar, user=user)
    return render(request, 'calendar.html', {'calendar': calendar})

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
    
def event_list(request):
    events = Event.objects.all()
    event_list = [{
        'title': event.title,
        'start': event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        'end': event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
    } for event in events]
    return JsonResponse(event_list, safe=False)

@login_required
@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        # Extract event details from request.POST or request.body
        title = request.POST.get('title')
        start_time = request.POST.get('start')
        end_time = request.POST.get('end')
        
        # Create the event, ensuring to include the user
        event = Event.objects.create(
            title=title,
            start_time=start_time,
            end_time=end_time,
            user=request.user  # Assign the logged-in user to the event
        )
        
        # Return a success response
        return JsonResponse({'status': 'success', 'event_id': event.id})
    else:
        # Handle non-POST requests here
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)