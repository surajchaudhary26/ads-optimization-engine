from typing import Dict
from app.api.schemas import AdInput


def extract_features(ad: AdInput) -> Dict[str, float]:
    clicks = ad.clicks
    conversions = ad.conversions

    conversion_rate = conversions / clicks if clicks > 0 else 0.0

    return {
        "cost": float(ad.cost),
        "priority": float(ad.priority),
        "clicks": float(clicks),
        "conversions": float(conversions),
        "conversion_rate": float(conversion_rate)
    }
