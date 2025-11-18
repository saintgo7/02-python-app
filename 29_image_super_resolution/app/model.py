import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import numpy as np
from pathlib import Path
from typing import Union, List


class EsrganModel(nn.Module):
    """PyTorch model for esrgan"""

    def __init__(self, input_size: int = 224, num_classes: int = 1000):
        super().__init__()
        self.input_size = input_size
        self.num_classes = num_classes

        # Feature extraction
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1))
        )

        # Classification head
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(128, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x


class ModelInference:
    """Inference wrapper for esrgan"""

    def __init__(self, model_path: Union[str, Path] = None, device: str = "cpu"):
        self.device = torch.device(device)
        self.model = EsrganModel().to(self.device)

        if model_path:
            self.load_model(model_path)

        self.model.eval()

    def load_model(self, model_path: Union[str, Path]):
        """Load trained model"""
        checkpoint = torch.load(model_path, map_location=self.device)
        if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
            self.model.load_state_dict(checkpoint["model_state_dict"])
        else:
            self.model.load_state_dict(checkpoint)

    def save_model(self, model_path: Union[str, Path]):
        """Save model"""
        torch.save(self.model.state_dict(), model_path)

    def predict(self, x: torch.Tensor) -> np.ndarray:
        """Run inference"""
        with torch.no_grad():
            x = x.to(self.device)
            outputs = self.model(x)
            probabilities = torch.softmax(outputs, dim=1)
            return probabilities.cpu().numpy()

    def predict_batch(self, images: List[np.ndarray]) -> np.ndarray:
        """Batch prediction"""
        inputs = torch.tensor(np.stack(images), dtype=torch.float32)
        return self.predict(inputs)


# Training function
def train_epoch(model, dataloader, optimizer, loss_fn, device):
    """Train for one epoch"""
    model.train()
    total_loss = 0.0

    for batch_idx, (images, labels) in enumerate(dataloader):
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = loss_fn(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(dataloader)
