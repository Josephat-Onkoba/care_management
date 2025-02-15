# prediction_service.py
from datetime import datetime, timedelta
from .models import DynamicData
from .prediction import prediction_model
from .encoding_utils import encode_meal_type, encode_stress_level  # Import encoding functions

def get_next_visit_prediction(care_recipient):
    """
    Fetches the latest dynamic data for a care recipient and predicts the next restroom visit time.

    Args:
        care_recipient (CareRecipient): The care recipient for whom to make the prediction.

    Returns:
        tuple: A tuple containing the predicted next visit time (datetime) and an error message (str).
               If the prediction fails, the predicted time will be None, and the error message will describe the issue.
    """
    # Fetch the latest dynamic data for the given care recipient
    latest_data = DynamicData.objects.filter(care_recipient=care_recipient).order_by('-timestamp').first()

    if not latest_data:
        return None, "No data available for prediction."

    # Prepare the feature dictionary
    features = {
        'water_intake_ml': latest_data.water_intake_ml,
        'physical_activity_steps': latest_data.physical_activity_steps,
        'sleep_duration_hours': float(latest_data.sleep_duration_hours) if latest_data.sleep_duration_hours else 0.0,
        'temperature': float(latest_data.temperature) if latest_data.temperature else 0.0,
        'humidity': float(latest_data.humidity) if latest_data.humidity else 0.0,
        'hours_since_last_visit': float(latest_data.hours_since_last_visit) if latest_data.hours_since_last_visit else 0.0,
        'duration_of_last_visit_seconds': latest_data.duration_of_last_visit_seconds or 0,
        'bladder_pressure': float(latest_data.bladder_pressure) if latest_data.bladder_pressure else 0.0,
        'heart_rate_variability': float(latest_data.heart_rate_variability) if latest_data.heart_rate_variability else 0.0,
        'body_temperature': float(latest_data.body_temperature) if latest_data.body_temperature else 0.0,
    }
    features['meal_type'] = encode_meal_type(latest_data.meal_type)
    features['stress_level'] = encode_stress_level(latest_data.stress_level)

    # Make a prediction using the model
    try:
        predicted_time_seconds = prediction_model.predict_one(features)
        if predicted_time_seconds:
            current_time = datetime.now()
            predicted_next_visit_time = current_time + timedelta(seconds=predicted_time_seconds)
            # Save the prediction to the database
            latest_data.predicted_next_visit_time = predicted_next_visit_time
            latest_data.save()
            return predicted_next_visit_time, None
        else:
            return None, "Prediction failed: Model returned no result."
    except Exception as e:
        return None, f"Prediction failed: {e}"