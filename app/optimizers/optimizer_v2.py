import pandas as pd
from typing import List, Dict

from app.api.schemas import AdInput
from app.features.feature_extractor import extract_features
from app.inference.model_loader import load_model


FEATURE_COLUMNS = [
    "cost",
    "priority",
    "clicks",
    "conversions",
    "conversion_rate"
]


def hybrid_score(ad: AdInput, ml_score: float) -> float:
    return (
        0.3 * (ml_score / 100.0)
        + 0.5 * ad.priority
        - 0.1 * ad.cost
    )


def optimize_ads_v2(
    ads: List[AdInput],
    total_budget: float
) -> Dict:
    """
    Production-safe Hybrid ML optimizer
    """

    # 🔹 SAFE model loading
    try:
        model = load_model()
    except Exception as e:
        print("❌ MODEL LOAD FAILED:", e)
        model = None   # fallback mode

    ranked_ads = []

    for ad in ads:
        features = extract_features(ad)

        X = pd.DataFrame(
            [[features[col] for col in FEATURE_COLUMNS]],
            columns=FEATURE_COLUMNS
        )

        # 🔹 SAFE prediction
        try:
            if model is not None:
                ml_score = float(model.predict(X)[0])
            else:
                ml_score = 0.0
        except Exception as e:
            print("⚠️ ML PREDICTION FAILED:", e)
            ml_score = 0.0

        final_score = hybrid_score(ad, ml_score)

        ranked_ads.append({
            "ad_id": ad.ad_id,
            "cost": ad.cost,
            "priority": ad.priority,
            "ml_score": round(ml_score, 2),
            "final_score": round(final_score, 2)
        })

    # 🔹 Rank by final score
    ranked_ads.sort(key=lambda x: x["final_score"], reverse=True)

    # 🔹 Budget selection
    selected_ads = []
    remaining_budget = total_budget

    for ad in ranked_ads:
        if ad["cost"] <= remaining_budget:
            selected_ads.append(ad)
            remaining_budget -= ad["cost"]

    return {
        "strategy": "hybrid_ml",
        "selected_ads": selected_ads,
        "total_cost": round(total_budget - remaining_budget, 2),
        "remaining_budget": round(remaining_budget, 2)
    }
