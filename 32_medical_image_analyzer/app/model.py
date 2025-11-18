import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import numpy as np
from pathlib import Path
from typing import Union, List, Tuple
import json


class Medical_ImageModel(models.Model):
    """TensorFlow medical_image Model"""

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
    """Transfer Learning wrapper for medical_image"""

    AVAILABLE_MODELS = ['MobileNetV2', 'ResNet50', 'InceptionV3', 'EfficientNetB0']

    def __init__(self, base_model_name: str = 'MobileNetV2', num_classes: int = 10):
        if base_model_name not in self.AVAILABLE_MODELS:
            raise ValueError(f"Model must be one of {self.AVAILABLE_MODELS}")

        self.base_model_name = base_model_name
        self.num_classes = num_classes
        self.model = self._build_model()

    def _build_model(self) -> models.Model:
        """Build transfer learning model"""
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
        """Compile model"""
        optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
        self.model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

    def train(self, x_train, y_train, x_val, y_val, epochs: int = 10, batch_size: int = 32):
        """Train model"""
        history = self.model.fit(
            x_train, y_train,
            validation_data=(x_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            verbose=1
        )
        return history

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if len(x.shape) == 3:
            x = np.expand_dims(x, axis=0)
        return self.model.predict(x, verbose=0)

    def save(self, path: Union[str, Path]):
        """Save model"""
        self.model.save(path)

    @staticmethod
    def load(path: Union[str, Path]) -> 'TransferLearningModel':
        """Load saved model"""
        model = keras.models.load_model(path)
        instance = TransferLearningModel.__new__(TransferLearningModel)
        instance.model = model
        return instance


class ModelEnsemble:
    """Ensemble multiple medical_image models"""

    def __init__(self, models_list: List = None):
        self.models = models_list or []

    def add_model(self, model):
        """Add model to ensemble"""
        self.models.append(model)

    def predict(self, x: np.ndarray, method: str = 'average') -> np.ndarray:
        """Make ensemble predictions"""
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
            raise ValueError(f"Unknown ensemble method: {method}")

    def save_ensemble(self, path: Union[str, Path]):
        """Save ensemble configuration"""
        config = {
            'num_models': len(self.models),
            'models': [f'model_{i}.h5' for i in range(len(self.models))]
        }
        with open(path / 'ensemble_config.json', 'w') as f:
            json.dump(config, f)

        for i, model in enumerate(self.models):
            model.save(path / f'model_{i}.h5')
