from typing import List, Dict
from app.api.schemas import AdInput


def select_ads_rule_based(
    ads: List[AdInput],
    total_budget: float
) -> Dict:

    selected_ads = []
    remaining_budget = total_budget

    ads_sorted = sorted(
        ads,
        key=lambda ad: (-ad.priority, ad.cost)
    )

    for ad in ads_sorted:
        if ad.cost <= remaining_budget:
            selected_ads.append({
                "ad_id": ad.ad_id,
                "cost": ad.cost,
                "priority": ad.priority
            })
            remaining_budget -= ad.cost

    return {
        "strategy": "rule_based",
        "selected_ads": selected_ads,
        "total_cost": total_budget - remaining_budget,
        "remaining_budget": remaining_budget
    }
