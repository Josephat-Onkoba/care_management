# core/utils/sms.py
import africastalking
from django.conf import settings

# Initialize Africa's Talking
africastalking.initialize(settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY)

# Get the SMS service
sms = africastalking.SMS

def send_sms(phone_number, message):
    """
    Sends an SMS using Africa's Talking.
    """
    try:
        # Send the SMS
        response = sms.send(message, [phone_number])
        print(f"SMS sent to {phone_number}: {response}")  # Debugging
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")  # Debugging
        return False