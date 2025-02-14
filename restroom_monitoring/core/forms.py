from django import forms
from .models import CareRecipient, DynamicData, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone_number']

    def save(self, commit=True):
        user = super().save(commit=commit)  # Save User model first
        if commit:
            Profile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])
        return user

class CareRecipientForm(forms.ModelForm):
    class Meta:
        model = CareRecipient
        fields = ['name', 'age', 'gender', 'bmi', 'medical_conditions']

class DynamicDataForm(forms.ModelForm):
    class Meta:
        model = DynamicData
        fields = [
            'water_intake_ml', 'physical_activity_steps', 'sleep_duration_hours', 'meal_type', 'specific_meal',
            'medication_taken', 'temperature', 'humidity', 'stress_level', 'hours_since_last_visit',
            'duration_of_last_visit_seconds', 'bladder_pressure', 'heart_rate_variability', 'body_temperature'
        ]

