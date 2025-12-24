from typing import Dict, Any


def generate_reason(ad: Dict[str, Any], rank: int) -> Dict[str, Any]:
    """
    Generates human-readable explanation for an ad.
    Backend is the single source of truth for explanation.
    """

    if rank == 1:
        label = "Best Choice"
        reason = (
            "This ad ranks highest due to strong predicted performance, "
            "high business priority, and efficient cost usage."
        )

    elif rank <= 3:
        label = "Good Choice"
        reason = (
            "This ad offers a good balance of predicted performance and "
            "business priority, but is slightly weaker than the top option."
        )

    else:
        label = "Consider Carefully"
        reason = (
            "This ad was selected within the budget but provides lower "
            "overall value compared to higher-ranked ads."
        )

    return {
        "rank": rank,
        "label": label,
        "reason": reason
    }
