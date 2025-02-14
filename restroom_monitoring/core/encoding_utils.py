# encoding_utils.py

def encode_meal_type(meal_type):
    """
    Encodes meal type into numerical values for the model.

    Args:
        meal_type (str): The meal type (e.g., 'Breakfast', 'Lunch').

    Returns:
        int: The encoded numerical value for the meal type.
    """
    meal_mapping = {'Breakfast': 1, 'Lunch': 2, 'Dinner': 3, 'Snack': 4}
    return meal_mapping.get(meal_type, 0)  # Default to 0 if meal_type is None or invalid

def encode_stress_level(stress_level):
    """
    Encodes stress level into numerical values for the model.

    Args:
        stress_level (str): The stress level (e.g., 'Low', 'Medium').

    Returns:
        int: The encoded numerical value for the stress level.
    """
    stress_mapping = {'Low': 1, 'Medium': 2, 'High': 3}
    return stress_mapping.get(stress_level, 0)  # Default to 0 if stress_level is None or invalid