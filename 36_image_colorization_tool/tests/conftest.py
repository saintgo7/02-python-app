import pytest
import numpy as np
import tempfile
from pathlib import Path


@pytest.fixture
def sample_image_array():
    """Create sample image array"""
    return np.random.rand(224, 224, 3).astype(np.float32)


@pytest.fixture
def sample_batch():
    """Create sample batch of images"""
    return np.random.rand(4, 224, 224, 3).astype(np.float32)


@pytest.fixture
def temp_model_dir():
    """Create temporary directory for models"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_model():
    """Create mock model"""
    class MockModel:
        def predict(self, x):
            batch_size = len(x) if isinstance(x, (list, np.ndarray)) else 1
            return np.random.rand(batch_size, 10).astype(np.float32)

    return MockModel()
