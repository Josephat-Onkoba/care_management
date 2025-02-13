# core/prediction.py
import numpy as np
from river import preprocessing, metrics, compose
from river.ensemble import BaggingRegressor
from river.linear_model import LinearRegression
from river.preprocessing import StandardScaler

class RestroomVisitPredictionModel:
    def __init__(self):
        # Use Bagging Regressor with Linear Regression as base estimator
        self.model = compose.Pipeline(
            ("scaler", preprocessing.StandardScaler()),
            ("regressor", BaggingRegressor(
                model=(LinearRegression()),
                n_models=5,
                seed=42
            ))
        )
        # Use MSE from metrics
        self.metric = metrics.MSE()
        self.model_data = []

    def update_model(self, new_data):
        """
        Updates the model with new data from the caregiver input
        """
        X = new_data.get('features', {})
        y = new_data.get('target', 0)
        
        try:
            # Learn from the new data point
            self.model = self.model.learn_one(X, y)
            
            # Predict and update metric
            y_pred = self.model.predict_one(X) if X else 0
            self.metric.update(y, y_pred)
            
            return y_pred
        except Exception as e:
            print(f"Error updating model: {e}")
            return None

    def predict_one(self, features):
        """
        Predict the next restroom visit based on input features
        """
        try:
            return self.model.predict_one(features)
        except Exception as e:
            print(f"Error predicting: {e}")
            return None

    def evaluate_model(self):
        """
        Evaluate the model performance using the accumulated metric
        """
        return self.metric.get()

# Initialize the model
prediction_model = RestroomVisitPredictionModel()