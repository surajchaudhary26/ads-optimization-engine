def validate_input(ads, total_budget):
    # 1. Check budget
    if total_budget is None:
        return False, "Total budget is required"

    if total_budget <= 0:
        return False, "Total budget must be greater than zero"

    # 2. Check ads list
    if not ads or len(ads) == 0:
        return False, "Ads list cannot be empty"

    # 3. Check each ad cost
    for ad in ads:
        if not hasattr(ad, "cost"):
            return False, "Each ad must have a cost"

        if ad.cost <= 0:
            return False, "Ad cost must be greater than zero"

    # If everything is fine
    return True, None
