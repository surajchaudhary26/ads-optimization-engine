def extract_features(ad: dict) -> dict:
    """
    Extract and compute ML features from raw ad input.

    This function is used in BOTH:
    - training pipeline
    - inference (optimizer_v2)

    Input:
        ad (dict): raw ad data

    Output:
        dict: engineered numerical features
    """

    clicks = ad.get("clicks", 0)
    conversions = ad.get("conversions", 0)

    # Safe conversion rate calculation
    conversion_rate = (
        conversions / clicks if clicks > 0 else 0.0
    )

    features = {
        "cost": float(ad.get("cost", 0)),
        "priority": int(ad.get("priority", 0)),
        "clicks": int(clicks),
        "conversions": int(conversions),
        "conversion_rate": float(conversion_rate),
    }

    return features
