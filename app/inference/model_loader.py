import joblib
from pathlib import Path
from typing import Any

MODEL_PATH = Path("artifacts/value_model.pkl")
_model: Any | None = None


def load_model() -> Any:
    global _model

    if _model is not None:
        return _model

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "ML model not found. Run training pipeline first."
        )

    _model = joblib.load(MODEL_PATH)
    return _model
