import pytest
import numpy as np
from app.batch_processor import BatchProcessor
from app.model_ensemble import ModelEnsemble


class TestBatchProcessor:
    """Test batch processor"""

    def test_batch_processor_initialization(self):
        """Test batch processor init"""
        processor = BatchProcessor(batch_size=32, max_workers=4)
        assert processor.batch_size == 32

    def test_process_single_batch(self, mock_model, sample_batch):
        """Test processing single batch"""
        processor = BatchProcessor(batch_size=4)
        results = processor.process_batch(mock_model, sample_batch)
        assert len(results) == 4

    def test_process_multiple_batches(self, mock_model):
        """Test processing multiple batches"""
        processor = BatchProcessor(batch_size=2)
        data = np.random.rand(5, 224, 224, 3).astype(np.float32)
        results = processor.process_batch(mock_model, data)
        assert len(results) == 5


class TestModelEnsemble:
    """Test model ensemble"""

    def test_ensemble_initialization(self):
        """Test ensemble init"""
        ensemble = ModelEnsemble()
        assert len(ensemble.models) == 0

    def test_add_model_to_ensemble(self, mock_model):
        """Test adding model to ensemble"""
        ensemble = ModelEnsemble()
        ensemble.add_model(mock_model, weight=1.0)
        assert len(ensemble.models) == 1

    def test_ensemble_prediction(self, mock_model, sample_image_array):
        """Test ensemble prediction"""
        ensemble = ModelEnsemble()
        ensemble.add_model(mock_model, weight=1.0)

        input_data = np.expand_dims(sample_image_array, axis=0)
        result = ensemble.predict_average(input_data)
        assert result is not None
        assert len(result) == 10
