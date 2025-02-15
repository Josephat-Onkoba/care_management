# prediction.py
from river import preprocessing, compose
from river.ensemble import BaggingRegressor
from river.linear_model import LinearRegression

class RestroomVisitPredictionModel:
    def __init__(self):
        """
        Initializes the prediction model using a pipeline with a scaler and a bagging regressor.
        """
        self.model = compose.Pipeline(
            ("scaler", preprocessing.StandardScaler()),
            ("regressor", BaggingRegressor(
                model=LinearRegression(),  # Base estimator
                n_models=5,  # Number of models in the ensemble
                seed=42  # Random seed for reproducibility
            ))
        )

    def learn_one(self, features, target):
        """
        Updates the model with a single data point.

        Args:
            features (dict): A dictionary of feature values.
            target (float): The target value (time until next visit in seconds).

        Returns:
            bool: True if the model was updated successfully, False otherwise.
        """
        try:
            self.model.learn_one(features, target)
            return True
        except Exception as e:
            print(f"Error updating model: {e}")
            return False

    def predict_one(self, features):
        """
        Predicts the time until the next restroom visit based on input features.

        Args:
            features (dict): A dictionary of feature values.

        Returns:
            float: Predicted time until the next visit in seconds, or None if prediction fails.
        """
        try:
            print("Features received for prediction:", features)  # Debugging: Print features
            prediction = self.model.predict_one(features)
            print("Prediction result:", prediction)  # Debugging: Print prediction
            return prediction
        except Exception as e:
            print(f"Error predicting: {e}")
            return None

# Initialize the model
prediction_model = RestroomVisitPredictionModel()