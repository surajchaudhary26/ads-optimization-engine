def select_ads_rule_based(ads, total_budget):
    selected_ads = []
    remaining_budget = total_budget

    for ad in ads:
        ad_cost = ad["cost"]

        if ad_cost <= remaining_budget:
            selected_ads.append(ad)
            remaining_budget -= ad_cost

    total_cost_used = total_budget - remaining_budget

    return selected_ads, total_cost_used
