import joblib
from pathlib import Path

MODEL_PATH = Path("artifacts/value_model.pkl")

if not MODEL_PATH.exists():
    """
    Load ML model once at startup.
    This keeps model loading centralized and reusable.
    """
    raise FileNotFoundError(
        "ML model not found. Please run training pipeline first."
    )

model = joblib.load(MODEL_PATH)