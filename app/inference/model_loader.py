import joblib
from pathlib import Path
from typing import Any

# app/inference/model_loader.py
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "artifacts" / "value_model.pkl"

_model: Any | None = None


def load_model() -> Any:
    global _model

    if _model is not None:
        return _model

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"ML model not found at {MODEL_PATH}"
        )

    _model = joblib.load(MODEL_PATH)
    return _model
