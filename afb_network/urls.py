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
    path('calendar/<int:user_id>/', views.calendar, name='calendar_url_name'),
    path('time_card/<int:user_id>/', views.time_card, name='time_card_url_name'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 