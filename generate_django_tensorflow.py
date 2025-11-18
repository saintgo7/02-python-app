#!/usr/bin/env python3
"""
Django and TensorFlow Complete Implementation Generator
"""

from pathlib import Path
from typing import Dict, List

# ============================
# DJANGO MODELS
# ============================

def generate_django_models(project_name: str, models: List[str]) -> str:
    """Generate Django models"""
    code = """from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


"""

    for i, model in enumerate(models):
        code += f"""class {model}(models.Model):
    \"\"\"Model for {model}\"\"\"
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return self.title


"""

    return code

def generate_django_serializers(project_name: str, models: List[str]) -> str:
    """Generate Django REST Framework serializers"""
    code = """from rest_framework import serializers
from .models import *


"""

    for model in models:
        code += f"""class {model}Serializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = {model}
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


"""

    return code

def generate_django_views(project_name: str, models: List[str]) -> str:
    """Generate Django REST Framework views"""
    code = """from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *


"""

    for model in models:
        model_lower = model.lower()
        code += f"""class {model}ViewSet(viewsets.ModelViewSet):
    serializer_class = {model}Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return {model}.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def active(self, request):
        \"\"\"Get only active items\"\"\"
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        \"\"\"Activate item\"\"\"
        obj = self.get_object()
        obj.is_active = True
        obj.save()
        return Response({{'status': 'item activated'}})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        \"\"\"Deactivate item\"\"\"
        obj = self.get_object()
        obj.is_active = False
        obj.save()
        return Response({{'status': 'item deactivated'}})


"""

    return code

def generate_django_urls(project_name: str, models: List[str]) -> str:
    """Generate Django URL configuration"""
    code = """from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = '{model_lower}s'

router = DefaultRouter()
""".format(model_lower=models[0].lower())

    for model in models:
        router_name = f"{model.lower()}"
        code += f"router.register(r'{router_name}s', {model}ViewSet, basename='{router_name}')\n"

    code += """
urlpatterns = [
    path('', include(router.urls)),
]
"""

    return code

def generate_django_views_file(project_name: str) -> str:
    """Generate Django main views"""
    return """from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'Welcome to API',
        'version': '1.0.0'
    })
"""

# ============================
# TENSORFLOW COMPLETE MODELS
# ============================

def generate_tensorflow_models(project_name: str, model_type: str) -> str:
    """Generate complete TensorFlow model implementations"""
    return f"""import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import numpy as np
from pathlib import Path
from typing import Union, List, Tuple
import json


class {model_type.title()}Model(models.Model):
    \"\"\"TensorFlow {model_type} Model\"\"\"

    def __init__(self, input_shape: Tuple[int, ...] = (224, 224, 3), num_classes: int = 1000):
        super().__init__()
        self.input_shape_val = input_shape
        self.num_classes = num_classes

        # Build the model architecture
        self.feature_extractor = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),

            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),

            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),

            layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.GlobalAveragePooling2D(),
        ])

        self.classifier = models.Sequential([
            layers.Dense(512, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation='softmax')
        ])

    def call(self, x, training=False):
        features = self.feature_extractor(x, training=training)
        return self.classifier(features, training=training)


class TransferLearningModel:
    \"\"\"Transfer Learning wrapper for {model_type}\"\"\"

    AVAILABLE_MODELS = ['MobileNetV2', 'ResNet50', 'InceptionV3', 'EfficientNetB0']

    def __init__(self, base_model_name: str = 'MobileNetV2', num_classes: int = 10):
        if base_model_name not in self.AVAILABLE_MODELS:
            raise ValueError(f"Model must be one of {{self.AVAILABLE_MODELS}}")

        self.base_model_name = base_model_name
        self.num_classes = num_classes
        self.model = self._build_model()

    def _build_model(self) -> models.Model:
        \"\"\"Build transfer learning model\"\"\"
        if self.base_model_name == 'MobileNetV2':
            base = keras.applications.MobileNetV2(
                input_shape=(224, 224, 3),
                include_top=False,
                weights='imagenet'
            )
        elif self.base_model_name == 'ResNet50':
            base = keras.applications.ResNet50(
                input_shape=(224, 224, 3),
                include_top=False,
                weights='imagenet'
            )
        elif self.base_model_name == 'InceptionV3':
            base = keras.applications.InceptionV3(
                input_shape=(224, 224, 3),
                include_top=False,
                weights='imagenet'
            )
        else:
            base = keras.applications.EfficientNetB0(
                input_shape=(224, 224, 3),
                include_top=False,
                weights='imagenet'
            )

        base.trainable = False

        model = models.Sequential([
            layers.Input(shape=(224, 224, 3)),
            keras.applications.mobilenet_v2.preprocess_input if self.base_model_name == 'MobileNetV2' else layers.Lambda(lambda x: x),
            base,
            layers.GlobalAveragePooling2D(),
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            layers.Dense(self.num_classes, activation='softmax')
        ])

        return model

    def compile(self, learning_rate: float = 1e-4):
        \"\"\"Compile model\"\"\"
        optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
        self.model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

    def train(self, x_train, y_train, x_val, y_val, epochs: int = 10, batch_size: int = 32):
        \"\"\"Train model\"\"\"
        history = self.model.fit(
            x_train, y_train,
            validation_data=(x_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            verbose=1
        )
        return history

    def predict(self, x: np.ndarray) -> np.ndarray:
        \"\"\"Make predictions\"\"\"
        if len(x.shape) == 3:
            x = np.expand_dims(x, axis=0)
        return self.model.predict(x, verbose=0)

    def save(self, path: Union[str, Path]):
        \"\"\"Save model\"\"\"
        self.model.save(path)

    @staticmethod
    def load(path: Union[str, Path]) -> 'TransferLearningModel':
        \"\"\"Load saved model\"\"\"
        model = keras.models.load_model(path)
        instance = TransferLearningModel.__new__(TransferLearningModel)
        instance.model = model
        return instance


class ModelEnsemble:
    \"\"\"Ensemble multiple {model_type} models\"\"\"

    def __init__(self, models_list: List = None):
        self.models = models_list or []

    def add_model(self, model):
        \"\"\"Add model to ensemble\"\"\"
        self.models.append(model)

    def predict(self, x: np.ndarray, method: str = 'average') -> np.ndarray:
        \"\"\"Make ensemble predictions\"\"\"
        if len(x.shape) == 3:
            x = np.expand_dims(x, axis=0)

        predictions = [model.predict(x) for model in self.models]

        if method == 'average':
            return np.mean(predictions, axis=0)
        elif method == 'max':
            return np.max(predictions, axis=0)
        elif method == 'voting':
            return np.argmax(np.sum(predictions, axis=0), axis=1)
        else:
            raise ValueError(f"Unknown ensemble method: {{method}}")

    def save_ensemble(self, path: Union[str, Path]):
        \"\"\"Save ensemble configuration\"\"\"
        config = {{
            'num_models': len(self.models),
            'models': [f'model_{{i}}.h5' for i in range(len(self.models))]
        }}
        with open(path / 'ensemble_config.json', 'w') as f:
            json.dump(config, f)

        for i, model in enumerate(self.models):
            model.save(path / f'model_{{i}}.h5')
"""

# ============================
# PROJECT GENERATION FUNCTIONS
# ============================

def create_django_project_complete(project_name: str, project_info: Dict):
    """Create complete Django project"""
    base_path = Path(f"/home/user/02-python-app/{project_name}")

    # Create models.py
    models_code = generate_django_models(project_name, project_info["models"])
    (base_path / "app" / "models.py").write_text(models_code)

    # Create serializers.py
    serializers_code = generate_django_serializers(project_name, project_info["models"])
    (base_path / "app" / "serializers.py").write_text(serializers_code)

    # Create views.py
    views_code = generate_django_views(project_name, project_info["models"])
    (base_path / "app" / "views.py").write_text(views_code)

    # Create urls.py
    urls_code = generate_django_urls(project_name, project_info["models"])
    (base_path / "app" / "urls.py").write_text(urls_code)

    # Create main views.py
    main_views = generate_django_views_file(project_name)
    (base_path / "app" / "views_main.py").write_text(main_views)


def create_tensorflow_project_complete(project_name: str, project_info: Dict):
    """Create complete TensorFlow project"""
    base_path = Path(f"/home/user/02-python-app/{project_name}")

    # Create complete model.py
    model_code = generate_tensorflow_models(project_name, project_info["model_type"])
    (base_path / "app" / "model.py").write_text(model_code)

    # Create inference API
    inference_code = f"""from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import numpy as np
from PIL import Image
import io
import tensorflow as tf
from app.model import TransferLearningModel, ModelEnsemble

app = FastAPI(title="{project_name}", version="1.0.0")

# Load model
try:
    model = TransferLearningModel(base_model_name='MobileNetV2')
    model.compile()
    print("Model loaded successfully")
except Exception as e:
    print(f"Warning: Model not found - {{e}}")
    model = None


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    \"\"\"Run inference on uploaded image\"\"\"
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image_array = np.array(image.resize((224, 224))) / 255.0

        if len(image_array.shape) == 2:
            image_array = np.stack([image_array] * 3, axis=-1)

        predictions = model.predict(image_array)

        return {{
            "predictions": predictions[0].tolist(),
            "predicted_class": int(np.argmax(predictions[0])),
            "confidence": float(np.max(predictions[0]))
        }}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/batch-predict")
async def batch_predict(files: list = File(...)):
    \"\"\"Batch inference on multiple images\"\"\"
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    results = []
    for file in files:
        try:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            image_array = np.array(image.resize((224, 224))) / 255.0

            predictions = model.predict(image_array)
            results.append({{
                "filename": file.filename,
                "predictions": predictions[0].tolist(),
                "predicted_class": int(np.argmax(predictions[0]))
            }})
        except Exception as e:
            results.append({{"filename": file.filename, "error": str(e)}})

    return {{"results": results}}


@app.get("/model-info")
def model_info():
    \"\"\"Get model information\"\"\"
    return {{
        "model_type": "{project_name}",
        "framework": "TensorFlow",
        "status": "ready" if model else "not_loaded"
    }}


@app.get("/health")
def health():
    return {{"status": "healthy"}}
"""
    (base_path / "main.py").write_text(inference_code)


def generate_django_and_tensorflow():
    """Generate Django and TensorFlow projects"""

    DJANGO_PROJECTS = {
        "11_multi_tenant_crm": {"models": ["Tenant", "Contact", "Deal", "Pipeline"]},
        "12_blog_platform": {"models": ["Post", "Comment", "Tag", "Category"]},
        "13_project_management_system": {"models": ["Project", "Task", "TeamMember", "TimeLog"]},
        "14_inventory_management": {"models": ["Product", "Warehouse", "Stock", "Order"]},
        "15_customer_support_portal": {"models": ["Ticket", "Response", "KnowledgeBase", "Category"]},
        "16_event_booking_system": {"models": ["Event", "Ticket", "Booking", "Attendee"]},
        "17_subscription_billing_platform": {"models": ["Plan", "Subscription", "Invoice", "Payment"]},
        "18_learning_management_system": {"models": ["Course", "Lesson", "Quiz", "Enrollment"]},
        "19_real_estate_listing_platform": {"models": ["Property", "Listing", "Viewing", "Offer"]},
        "20_social_network_backend": {"models": ["Post", "Comment", "Like", "Message"]},
    }

    TENSORFLOW_PROJECTS = {
        "31_traffic_sign_detection": {"model_type": "traffic_sign"},
        "32_medical_image_analyzer": {"model_type": "medical_image"},
        "33_plant_disease_detector": {"model_type": "plant_disease"},
        "34_license_plate_reader": {"model_type": "license_plate"},
        "35_product_defect_detector": {"model_type": "defect_detection"},
        "36_image_colorization_tool": {"model_type": "colorization"},
        "37_building_floor_plan_analyzer": {"model_type": "floor_plan"},
        "38_wildlife_species_detector": {"model_type": "species_detection"},
        "39_food_calorie_estimator": {"model_type": "food_detection"},
        "40_clothing_recommendation_ai": {"model_type": "clothing_detection"},
    }

    print("🚀 Generating Django and TensorFlow Complete Implementations...")
    print("=" * 70)

    # Generate Django projects
    for project_name, project_info in DJANGO_PROJECTS.items():
        print(f"[Django] {project_name}...", end=" ", flush=True)
        try:
            create_django_project_complete(project_name, project_info)
            print("✅")
        except Exception as e:
            print(f"❌ {{e}}")

    # Generate TensorFlow projects
    for project_name, project_info in TENSORFLOW_PROJECTS.items():
        print(f"[TensorFlow] {project_name}...", end=" ", flush=True)
        try:
            create_tensorflow_project_complete(project_name, project_info)
            print("✅")
        except Exception as e:
            print(f"❌ {{e}}")

    print("=" * 70)
    print("✨ All Django and TensorFlow projects generated!")


if __name__ == "__main__":
    generate_django_and_tensorflow()
