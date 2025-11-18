from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from typing import Dict, Tuple
import numpy as np
import json
from datetime import datetime


class ModelMetrics:
    """Track and monitor model performance metrics"""

    def __init__(self):
        self.metrics_history = []

    def calculate_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        average: str = "weighted"
    ) -> Dict[str, float]:
        """Calculate performance metrics"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "precision": float(precision_score(y_true, y_pred, average=average, zero_division=0)),
            "recall": float(recall_score(y_true, y_pred, average=average, zero_division=0)),
            "f1": float(f1_score(y_true, y_pred, average=average, zero_division=0)),
        }

        self.metrics_history.append(metrics)
        return metrics

    def get_confusion_matrix(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """Get confusion matrix"""
        return confusion_matrix(y_true, y_pred)

    def save_metrics(self, filepath: str):
        """Save metrics to file"""
        with open(filepath, "w") as f:
            json.dump(self.metrics_history, f, indent=2)

    def get_latest_metrics(self) -> Dict[str, float]:
        """Get latest metrics"""
        return self.metrics_history[-1] if self.metrics_history else {}

    def get_metrics_summary(self) -> Dict:
        """Get summary of all metrics"""
        if not self.metrics_history:
            return {}

        metrics_array = np.array([m for m in self.metrics_history if "accuracy" in m])
        keys = ["accuracy", "precision", "recall", "f1"]

        summary = {}
        for key in keys:
            values = [m[key] for m in self.metrics_history if key in m]
            if values:
                summary[key] = {
                    "mean": float(np.mean(values)),
                    "std": float(np.std(values)),
                    "min": float(np.min(values)),
                    "max": float(np.max(values)),
                }

        return summary
