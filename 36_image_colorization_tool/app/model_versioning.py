import json
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
