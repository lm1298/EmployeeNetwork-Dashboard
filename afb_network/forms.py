from django import forms
from .models import EmployeeProfile

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