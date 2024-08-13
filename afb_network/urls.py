from django.urls import include, path
from django.contrib.auth.views import LoginView
from django.contrib import admin
from . import views  # Make sure to import your app's views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/', include('allauth.urls')),
    path('', views.profile_page, name='profile'),
    path('talk/<int:user_id>/', views.talk, name='talk_url_name'),
    path('calendar/<int:user_id>/', views.user_calendar, name='user_calendar'),
    path('calendar/add/', views.add_event, name='add_event'),
    path('events/<int:user_id>', views.event_list, name='event-list'),
    path('timecard/<int:user_id>/', views.user_timecard, name='user_timecard'),
    #path('timecard/<int:user_id>/add/', views.add_time_entry, name='add_time_entry'),
    path('edit/<int:timecard_id>/', views.edit_timecard, name='edit_timecard'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 