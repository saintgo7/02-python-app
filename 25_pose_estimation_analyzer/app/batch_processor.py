import asyncio
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
