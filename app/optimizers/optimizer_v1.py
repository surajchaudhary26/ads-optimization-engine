def select_ads_rule_based(ads, total_budget):
    """
    Rule-based ad selection logic.

    Strategy:
    1. Sort ads by priority (high to low)
    2. Within same priority, sort by cost (low to high)
    3. Select ads greedily until budget is exhausted
    """

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

    total_cost_used = total_budget - remaining_budget

    return selected_ads, total_cost_used
