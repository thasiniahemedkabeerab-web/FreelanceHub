from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Job
from .models import JobApplication
from .models import FreelancerProfile
class SignupForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'role',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control login-input'

        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Create password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'



class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title',
            'category',
            'description',
            'budget',
            'deadline'
        ]

        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['proposal', 'bid_amount']

from .models import FreelancerProfile

class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = [
            'profile_image',
            'title',
            'bio',
            'skills',
            'hourly_rate',
            'experience',
            'location'
        ]