import joblib
import numpy as np
from pathlib import Path

from app.features.feature_extractor import extract_features


# -------------------------------
# Load ML model ONCE (at startup)
# -------------------------------
MODEL_PATH = Path("artifacts/value_model.pkl")

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        "ML model not found. Please run training pipeline first."
    )

model = joblib.load(MODEL_PATH)


def hybrid_score(ad, ml_score):
    """
    Combine business rules + ML score
    HYBRID decision logic
    """

    ml_score_norm = ml_score / 100  

    priority_weight = ad["priority"] * 0.5
    cost_penalty = ad["cost"] * 0.1

    final_score = (
        0.3 * ml_score_norm
        + priority_weight
        - cost_penalty
    )

    return final_score


def optimize_ads_v2(ads):
    """
    Hybrid optimizer:
    - assumes data is already validated
    - uses ML score + business logic
    """

    optimized_ads = []

    for ad in ads:
        features = extract_features(ad)

        X = np.array([[
            features["cost"],
            features["priority"],
            features["clicks"],
            features["conversions"],
            features["conversion_rate"]
        ]])

        ml_score = model.predict(X)[0]
        final_score = hybrid_score(ad, ml_score)

        optimized_ads.append({
            "ad_id": ad["ad_id"],
            "cost": ad["cost"],
            "ml_score": round(float(ml_score), 2),
            "final_score": round(float(final_score), 2)
        })

    optimized_ads.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return optimized_ads
