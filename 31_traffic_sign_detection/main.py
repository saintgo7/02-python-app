from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import numpy as np
from PIL import Image
import io
import tensorflow as tf
from app.model import TransferLearningModel, ModelEnsemble

app = FastAPI(title="31_traffic_sign_detection", version="1.0.0")

# Load model
try:
    model = TransferLearningModel(base_model_name='MobileNetV2')
    model.compile()
    print("Model loaded successfully")
except Exception as e:
    print(f"Warning: Model not found - {e}")
    model = None


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Run inference on uploaded image"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image_array = np.array(image.resize((224, 224))) / 255.0

        if len(image_array.shape) == 2:
            image_array = np.stack([image_array] * 3, axis=-1)

        predictions = model.predict(image_array)

        return {
            "predictions": predictions[0].tolist(),
            "predicted_class": int(np.argmax(predictions[0])),
            "confidence": float(np.max(predictions[0]))
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/batch-predict")
async def batch_predict(files: list = File(...)):
    """Batch inference on multiple images"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    results = []
    for file in files:
        try:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            image_array = np.array(image.resize((224, 224))) / 255.0

            predictions = model.predict(image_array)
            results.append({
                "filename": file.filename,
                "predictions": predictions[0].tolist(),
                "predicted_class": int(np.argmax(predictions[0]))
            })
        except Exception as e:
            results.append({"filename": file.filename, "error": str(e)})

    return {"results": results}


@app.get("/model-info")
def model_info():
    """Get model information"""
    return {
        "model_type": "31_traffic_sign_detection",
        "framework": "TensorFlow",
        "status": "ready" if model else "not_loaded"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
