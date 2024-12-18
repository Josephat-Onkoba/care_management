from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CareRecipient, DynamicData
from .forms import CareRecipientForm, DynamicDataForm
from django.contrib import messages

# Caregiver Signup
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

# Dashboard
@login_required
def dashboard(request):
    care_recipients = request.user.care_recipients.all()
    return render(request, 'core/dashboard.html', {'care_recipients': care_recipients})

# Add Care Recipient
@login_required
def add_care_recipient(request):
    if request.method == 'POST':
        form = CareRecipientForm(request.POST)
        if form.is_valid():
            care_recipient = form.save(commit=False)
            care_recipient.caregiver = request.user
            care_recipient.save()
            return redirect('dashboard')
    else:
        form = CareRecipientForm()
    return render(request, 'core/add_care_recipient.html', {'form': form})

# View Care Recipient Dashboard
@login_required
def view_care_recipient(request, id):
    care_recipient = get_object_or_404(CareRecipient, id=id, caregiver=request.user)
    dynamic_data = care_recipient.dynamic_data.all()
    return render(request, 'core/care_recipient_dashboard.html', {
        'care_recipient': care_recipient,
        'dynamic_data': dynamic_data,
    })

# Add Dynamic Data
@login_required
def add_dynamic_data(request, id):
    care_recipient = get_object_or_404(CareRecipient, id=id, caregiver=request.user)
    
    if request.method == 'POST':
        form = DynamicDataForm(request.POST)
        if form.is_valid():
            dynamic_data = form.save(commit=False)
            dynamic_data.care_recipient = care_recipient
            dynamic_data.save()
            messages.success(request, "Dynamic data added successfully!")
            return redirect('view_care_recipient', id=id)
    else:
        form = DynamicDataForm()
    
    context = {
        'form': form,
        'care_recipient': care_recipient  # Adding this might be useful in the template
    }
    return render(request, 'core/add_dynamic_data.html', context)
