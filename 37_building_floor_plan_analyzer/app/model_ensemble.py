from typing import List, Dict
import numpy as np


class ModelEnsemble:
    """Ensemble multiple models for better predictions"""

    def __init__(self, models: List = None, weights: List[float] = None):
        self.models = models or []
        self.weights = weights or [1.0 / len(self.models)] * len(self.models)

    def add_model(self, model, weight: float = 1.0):
        """Add model to ensemble"""
        self.models.append(model)
        total_weight = sum(self.weights) + weight
        self.weights = [w / total_weight for w in self.weights]
        self.weights.append(weight / total_weight)

    def predict_average(self, x: np.ndarray) -> np.ndarray:
        """Average ensemble predictions"""
        predictions = []

        for model in self.models:
            pred = model.predict(x)
            predictions.append(pred)

        predictions = np.array(predictions)
        return np.average(predictions, axis=0, weights=self.weights)

    def predict_voting(self, x: np.ndarray) -> np.ndarray:
        """Voting ensemble (for classification)"""
        predictions = []

        for model in self.models:
            pred = model.predict(x)
            predictions.append(np.argmax(pred, axis=1))

        predictions = np.array(predictions)
        return np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=predictions)

    def predict_weighted(self, x: np.ndarray) -> np.ndarray:
        """Weighted ensemble predictions"""
        weighted_predictions = np.zeros_like(self.models[0].predict(x))

        for model, weight in zip(self.models, self.weights):
            pred = model.predict(x)
            weighted_predictions += pred * weight

        return weighted_predictions
