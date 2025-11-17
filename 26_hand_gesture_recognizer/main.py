from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import numpy as np
import torch
from PIL import Image
import io
from app.model import ModelInference

app = FastAPI(title="26_hand_gesture_recognizer", version="1.0.0")

# Load model
model = ModelInference(device="cpu")


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Run inference on uploaded image"""
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image_array = np.array(image.resize((224, 224))) / 255.0

    predictions = model.predict(torch.from_numpy(image_array).unsqueeze(0).float())

    return {"predictions": predictions.tolist()}


@app.get("/health")
def health():
    return {"status": "healthy"}
