from datetime import datetime, timedelta
from .models import DynamicData
from .prediction import prediction_model


def stream_data_for_prediction(care_recipient_id):
    """
    Streams dynamic data from the database, processes it for numerical compatibility,
    and feeds it into the model to predict the next restroom visit time.
    """
    # Fetch the latest 20 entries for the care recipient
    data_stream = DynamicData.objects.filter(care_recipient_id=care_recipient_id).order_by('-timestamp')[:20]

    for data in reversed(data_stream):  # Reverse to feed the oldest entries first
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

        # Encode categorical fields
        features['meal_type'] = encode_meal_type(data.meal_type)
        features['stress_level'] = encode_stress_level(data.stress_level)

        try:
            # Update the model with the feature set
            prediction_model.learn_one(features, None)
            print("Model updated with new data.")
        except Exception as e:
            print(f"Error updating model: {e}")

        try:
            # Make a prediction
            predicted_time_seconds = prediction_model.predict_one(features)

            if predicted_time_seconds:
                # Calculate the predicted time
                current_time = datetime.now()
                predicted_time = current_time + timedelta(seconds=predicted_time_seconds)

                # Save the predicted next visit time in the database
                data.predicted_next_visit_time = predicted_time
                data.save()

                print(f"Next visit predicted at: {predicted_time.strftime('%Y-%m-%d %H:%M:%S')}")

            else:
                print("No prediction could be made.")

        except Exception as e:
            print(f"Error predicting: {e}")

    return "Streaming completed."


def encode_meal_type(meal_type):
    """
    Encodes meal type into numerical values for the model.
    """
    meal_mapping = {'Breakfast': 1, 'Lunch': 2, 'Dinner': 3, 'Snack': 4}
    return meal_mapping.get(meal_type, 0)  # Default to 0 if meal_type is None or invalid


def encode_stress_level(stress_level):
    """
    Encodes stress level into numerical values for the model.
    """
    stress_mapping = {'low': 1, 'medium': 2, 'high': 3}
    return stress_mapping.get(stress_level, 0)  # Default to 0 if stress_level is None or invalid
