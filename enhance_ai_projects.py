#!/usr/bin/env python3
"""
AI Project Enhancement
Adds advanced features to AI projects:
- Batch processing
- Model ensemble
- Async inference
- Model versioning
- Performance metrics
"""

from pathlib import Path

def generate_batch_processor() -> str:
    """Generate batch processing utility"""
    return '''import asyncio
from typing import List, Tuple
import numpy as np
from concurrent.futures import ThreadPoolExecutor


class BatchProcessor:
    """Batch processing for model inference"""

    def __init__(self, batch_size: int = 32, max_workers: int = 4):
        self.batch_size = batch_size
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def process_batch(self, model, images: List[np.ndarray]) -> List[np.ndarray]:
        """Process images in batches"""
        results = []

        for i in range(0, len(images), self.batch_size):
            batch = images[i : i + self.batch_size]
            batch_array = np.array(batch)

            predictions = model.predict(batch_array)
            results.extend(predictions)

        return results

    async def async_process_batch(self, model, images: List[np.ndarray]) -> List[np.ndarray]:
        """Async batch processing"""
        loop = asyncio.get_event_loop()

        return await loop.run_in_executor(
            self.executor,
            self.process_batch,
            model,
            images
        )

    def process_with_callbacks(
        self,
        model,
        images: List[np.ndarray],
        callback=None,
        on_complete=None
    ) -> List[np.ndarray]:
        """Process with progress callbacks"""
        results = []
        total = len(images)

        for i in range(0, total, self.batch_size):
            batch = images[i : i + self.batch_size]
            batch_array = np.array(batch)

            predictions = model.predict(batch_array)
            results.extend(predictions)

            # Progress callback
            if callback:
                progress = (i + len(batch)) / total
                callback(progress)

        # Complete callback
        if on_complete:
            on_complete()

        return results
'''


def generate_model_ensemble() -> str:
    """Generate model ensemble"""
    return '''from typing import List, Dict
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
'''


def generate_model_metrics() -> str:
    """Generate model metrics and monitoring"""
    return '''from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
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
'''


def generate_model_versioning() -> str:
    """Generate model versioning system"""
    return '''import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional


class ModelVersioning:
    """Manage model versions and checkpoints"""

    def __init__(self, model_dir: str = "models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
        self.manifest_file = self.model_dir / "manifest.json"

    def save_version(
        self,
        model,
        version: str,
        metrics: Dict = None,
        notes: str = ""
    ) -> bool:
        """Save model version"""
        try:
            version_dir = self.model_dir / version
            version_dir.mkdir(exist_ok=True)

            # Save model
            model_path = version_dir / "model.h5"
            model.save(model_path)

            # Save metadata
            metadata = {
                "version": version,
                "timestamp": datetime.now().isoformat(),
                "metrics": metrics or {},
                "notes": notes,
            }

            metadata_path = version_dir / "metadata.json"
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)

            # Update manifest
            self._update_manifest(version, metadata)

            return True
        except Exception as e:
            print(f"Error saving version: {e}")
            return False

    def load_version(self, version: str):
        """Load model version"""
        try:
            version_dir = self.model_dir / version
            model_path = version_dir / "model.h5"

            if not model_path.exists():
                raise FileNotFoundError(f"Model {version} not found")

            import keras
            model = keras.models.load_model(model_path)
            return model
        except Exception as e:
            print(f"Error loading version: {e}")
            return None

    def get_versions(self) -> list:
        """Get all available versions"""
        versions = []

        for version_dir in self.model_dir.iterdir():
            if version_dir.is_dir():
                metadata_file = version_dir / "metadata.json"
                if metadata_file.exists():
                    with open(metadata_file) as f:
                        metadata = json.load(f)
                        versions.append(metadata)

        return sorted(versions, key=lambda x: x["timestamp"], reverse=True)

    def delete_version(self, version: str) -> bool:
        """Delete model version"""
        try:
            version_dir = self.model_dir / version
            shutil.rmtree(version_dir)
            self._update_manifest(version, None)
            return True
        except Exception as e:
            print(f"Error deleting version: {e}")
            return False

    def _update_manifest(self, version: str, metadata: Optional[Dict]):
        """Update manifest file"""
        manifest = {}

        if self.manifest_file.exists():
            with open(self.manifest_file) as f:
                manifest = json.load(f)

        if metadata is None:
            manifest.pop(version, None)
        else:
            manifest[version] = metadata

        with open(self.manifest_file, "w") as f:
            json.dump(manifest, f, indent=2)
'''


def generate_enhanced_ai_main() -> str:
    """Generate enhanced main.py for AI projects"""
    return '''from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import numpy as np
from PIL import Image
import io
import json
from app.batch_processor import BatchProcessor
from app.model_ensemble import ModelEnsemble
from app.model_metrics import ModelMetrics
from app.model_versioning import ModelVersioning

app = FastAPI(
    title="Advanced AI Model API",
    version="1.0.0",
    description="AI model with batch processing, ensemble, metrics, and versioning"
)

# Initialize components
batch_processor = BatchProcessor(batch_size=32)
model_metrics = ModelMetrics()
model_versioning = ModelVersioning()
ensemble = ModelEnsemble()

# Placeholder for actual model
model = None


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Single image prediction"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image_array = np.array(image.resize((224, 224))) / 255.0

        prediction = model.predict(np.expand_dims(image_array, axis=0))

        return {
            "predictions": prediction[0].tolist(),
            "predicted_class": int(np.argmax(prediction[0])),
            "confidence": float(np.max(prediction[0]))
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict-batch")
async def predict_batch(files: list = File(...)):
    """Batch prediction"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        images = []
        filenames = []

        for file in files:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            image_array = np.array(image.resize((224, 224))) / 255.0
            images.append(image_array)
            filenames.append(file.filename)

        predictions = batch_processor.process_batch(model, images)

        results = []
        for filename, pred in zip(filenames, predictions):
            results.append({
                "filename": filename,
                "predictions": pred.tolist(),
                "predicted_class": int(np.argmax(pred)),
                "confidence": float(np.max(pred))
            })

        return {"results": results, "total": len(results)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/metrics")
def get_metrics():
    """Get latest metrics"""
    latest = model_metrics.get_latest_metrics()
    summary = model_metrics.get_metrics_summary()

    return {
        "latest": latest,
        "summary": summary,
        "total_predictions": len(model_metrics.metrics_history)
    }


@app.get("/versions")
def get_versions():
    """Get all model versions"""
    versions = model_versioning.get_versions()
    return {"versions": versions}


@app.post("/save-version/{version_id}")
def save_version(version_id: str, notes: str = ""):
    """Save current model as version"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    metrics = model_metrics.get_latest_metrics()
    success = model_versioning.save_version(model, version_id, metrics, notes)

    if success:
        return {"message": f"Model saved as {version_id}"}
    else:
        raise HTTPException(status_code=500, detail="Failed to save version")


@app.get("/load-version/{version_id}")
def load_version(version_id: str):
    """Load specific model version"""
    global model
    model = model_versioning.load_version(version_id)

    if model is None:
        raise HTTPException(status_code=404, detail=f"Version {version_id} not found")

    return {"message": f"Model {version_id} loaded"}


@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}
'''


def enhance_ai_projects():
    """Enhance AI projects"""
    ai_projects = (
        list(range(21, 31)) +  # PyTorch
        list(range(31, 41))    # TensorFlow
    )

    ai_project_names = [f"{i:02d}_" for i in ai_projects]

    print("🚀 Enhancing AI Projects with Advanced Features...")
    print("=" * 70)

    for i in ai_projects:
        projects = list(Path("/home/user/02-python-app").glob(f"{i:02d}_*"))
        if not projects:
            continue

        project_name = projects[0].name
        base_path = projects[0]
        print(f"[{project_name}]", end=" ", flush=True)

        try:
            # Create batch processor
            batch_code = generate_batch_processor()
            (base_path / "app" / "batch_processor.py").write_text(batch_code)

            # Create ensemble
            ensemble_code = generate_model_ensemble()
            (base_path / "app" / "model_ensemble.py").write_text(ensemble_code)

            # Create metrics
            metrics_code = generate_model_metrics()
            (base_path / "app" / "model_metrics.py").write_text(metrics_code)

            # Create versioning
            versioning_code = generate_model_versioning()
            (base_path / "app" / "model_versioning.py").write_text(versioning_code)

            # Update main.py
            enhanced_main = generate_enhanced_ai_main()
            (base_path / "main.py").write_text(enhanced_main)

            # Update requirements
            enhanced_requirements = '''torch==2.1.2
torchvision==0.16.2
tensorflow==2.15.0
fastapi==0.104.1
uvicorn==0.24.0
pillow==10.1.0
opencv-python==4.8.1.78
numpy==1.24.3
scipy==1.11.4
scikit-learn==1.3.2
pytest==7.4.3

# Advanced features
aiofiles==23.2.1
python-multipart==0.0.6
'''
            (base_path / "requirements.txt").write_text(enhanced_requirements)

            print("✅")
        except Exception as e:
            print(f"❌ Error: {e}")

    print("=" * 70)
    print("✨ AI projects enhanced!")


if __name__ == "__main__":
    enhance_ai_projects()
