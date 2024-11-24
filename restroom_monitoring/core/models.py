from django.db import models
from django.contrib.auth.models import User

# Care Recipient Model
class CareRecipient(models.Model):
    caregiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="care_recipients")
    name = models.CharField(max_length=100)  # Name of the care recipient
    age = models.PositiveIntegerField()  # Age in years
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    bmi = models.DecimalField(max_digits=5, decimal_places=2)  # Body Mass Index
    medical_conditions = models.TextField(blank=True, null=True)  # Medical conditions affecting bladder/bowel

    def __str__(self):
        return self.name

# Dynamic Data Model
class DynamicData(models.Model):
    care_recipient = models.ForeignKey(CareRecipient, on_delete=models.CASCADE, related_name="dynamic_data")
    timestamp = models.DateTimeField(auto_now_add=True)
    water_intake_ml = models.IntegerField()  # Water/beverage intake in milliliters
    physical_activity_steps = models.IntegerField(blank=True, null=True)  # Physical activity levels (steps)
    sleep_duration_hours = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)  # Sleep duration
    meal_type = models.CharField(max_length=50, choices=[
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack')
    ])
    specific_meal = models.CharField(max_length=255, blank=True, null=True)  # Specific meal details
    medication_taken = models.TextField(blank=True, null=True)  # Medication details
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    humidity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    stress_level = models.CharField(max_length=10, choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ], blank=True, null=True)
    hours_since_last_visit = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    duration_of_last_visit_seconds = models.IntegerField(blank=True, null=True)
    bladder_pressure = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    heart_rate_variability = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    body_temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Data for {self.care_recipient.name} at {self.timestamp}"
