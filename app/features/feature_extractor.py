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

    clicks = ad.clicks
    conversions = ad.conversions
    cost = ad.cost
    priority = ad.priority

    # Safe conversion rate calculation
    
    conversion_rate = conversions / clicks if clicks > 0 else 0.0

    return {
        "cost": cost,
        "priority": priority,
        "clicks": clicks,
        "conversions": conversions,
        "conversion_rate": conversion_rate
    }
