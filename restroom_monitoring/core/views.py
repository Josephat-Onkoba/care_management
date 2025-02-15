from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CareRecipient, DynamicData
from .forms import CareRecipientForm, DynamicDataForm
from django.contrib import messages
from .prediction_service import get_next_visit_prediction
from .prediction_stream import stream_data_for_prediction  # Import the streaming function
from .utils.sms import send_sms

# Caregiver Signup
from .forms import CustomUserCreationForm  
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
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
@login_required
def view_care_recipient(request, id):
    try:
        care_recipient = get_object_or_404(CareRecipient, id=id, caregiver=request.user)
        dynamic_data = DynamicData.objects.filter(care_recipient=care_recipient).order_by('-timestamp')

        # Train the model with historical data
        stream_data_for_prediction(care_recipient.id)

        # Get the next visit prediction
        predicted_next_visit, prediction_error = get_next_visit_prediction(care_recipient)

        # Send SMS notification if a prediction is made
        if predicted_next_visit:
            caregiver_profile = care_recipient.caregiver.profile
            if caregiver_profile.phone_number:
                message = (
                    f"Predicted next restroom visit for {care_recipient.name}: "
                    f"{predicted_next_visit.strftime('%Y-%m-%d %H:%M:%S')}"
                )
                send_sms(caregiver_profile.phone_number, message)

        context = {
            'care_recipient': care_recipient,
            'dynamic_data': dynamic_data,
            'predicted_next_visit': predicted_next_visit,
            'prediction_error': prediction_error,
        }
        return render(request, 'core/view_care_recipient.html', context)
    except Exception as e:
        print(f"Error in view_care_recipient: {e}")  # Debugging
        return render(request, 'core/500.html', status=500)


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

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return render(request, 'core/logout.html') 