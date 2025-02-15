from twilio.rest import Client
from django.conf import settings

def send_sms(to_phone_number, message):
    """
    Sends an SMS using Twilio.
    """
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_phone_number
        )
        print(f"SMS sent to {to_phone_number}: {message.sid}")  # Debugging
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")  # Debugging
        return False