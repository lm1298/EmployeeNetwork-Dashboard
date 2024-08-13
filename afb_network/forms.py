from django import forms
from .models import EmployeeProfile, Event, TimeEntry

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = '__all__'
    
    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 2.5 * 1024 * 1024:  # Limit image size to 2.5MB
                raise forms.ValidationError("Image file too large ( > 2.5MB )")
            return image.read()
        else:
            return None
        
class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['work_hours', 'work_minutes', 'summary', 'date', 'vacation']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'start_time', 'end_time']
