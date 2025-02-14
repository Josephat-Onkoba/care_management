from datetime import datetime
from .models import DynamicData
from .prediction import prediction_model
from .encoding_utils import encode_meal_type, encode_stress_level
from django.utils import timezone  # Import Django's timezone utility
import random

def stream_data_for_prediction(care_recipient_id):
    """
    Streams dynamic data from the database, processes it for numerical compatibility,
    and feeds it into the model to predict the next restroom visit time.
    """
    try:
        print(f"Fetching data for care recipient ID: {care_recipient_id}")  # Debugging
        # Fetch the latest 20 entries for the care recipient
        data_stream = DynamicData.objects.filter(care_recipient_id=care_recipient_id).order_by('-timestamp')[:20]

        if not data_stream:
            print(f"No data found for care recipient ID: {care_recipient_id}")  # Debugging
            return "No data available."

        print(f"Found {len(data_stream)} data entries for care recipient ID: {care_recipient_id}")  # Debugging
        for data in reversed(data_stream):  # Reverse to feed the oldest entries first
            print(f"Processing data ID: {data.id}")  # Debugging
            # Prepare the feature dictionary
            features = {
                'water_intake_ml': data.water_intake_ml,
                'physical_activity_steps': data.physical_activity_steps,
                'sleep_duration_hours': float(data.sleep_duration_hours) if data.sleep_duration_hours else 0.0,
                'temperature': float(data.temperature) if data.temperature else 0.0,
                'humidity': float(data.humidity) if data.humidity else 0.0,
                'hours_since_last_visit': float(data.hours_since_last_visit) if data.hours_since_last_visit else 0.0,
                'duration_of_last_visit_seconds': data.duration_of_last_visit_seconds or 0,
                'bladder_pressure': float(data.bladder_pressure) if data.bladder_pressure else 0.0,
                'heart_rate_variability': float(data.heart_rate_variability) if data.heart_rate_variability else 0.0,
                'body_temperature': float(data.body_temperature) if data.body_temperature else 0.0,
            }
            features['meal_type'] = encode_meal_type(data.meal_type)
            features['stress_level'] = encode_stress_level(data.stress_level)

            # Calculate the target value (time_until_next_visit_seconds)
            if data.predicted_next_visit_time:
                current_time = timezone.now()  # Use timezone-aware datetime
                predicted_visit_time = data.predicted_next_visit_time
                time_until_next_visit_seconds = (predicted_visit_time - current_time).total_seconds()
            else:
                time_until_next_visit_seconds = random.randint(1800, 7200)
                print(f"Using random time_until_next_visit_seconds: {time_until_next_visit_seconds}")  # Debugging

            try:
                # Update the model with the feature set and target value
                prediction_model.learn_one(features, time_until_next_visit_seconds)
                print(f"Model updated with data ID: {data.id}")  # Debugging
            except Exception as e:
                print(f"Error updating model with data ID {data.id}: {e}")  # Debugging

        return "Streaming completed."
    except Exception as e:
        print(f"Error in stream_data_for_prediction: {e}")  # Debugging
        raise  # Re-raise the exception to see the full traceback in the logs