from fastapi import FastAPI, UploadFile, File, HTTPException
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
