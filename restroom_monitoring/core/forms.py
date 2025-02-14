from django import forms
from .models import CareRecipient, DynamicData

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

