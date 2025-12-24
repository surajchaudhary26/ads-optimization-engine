from typing import List, Tuple
from app.api.schemas import AdInput


def validate_input(
    ads: List[AdInput],
    total_budget: float
) -> Tuple[bool, str | None]:

    # 1. Budget validation
    if total_budget <= 0:
        return False, "Total budget must be greater than zero"

    # 2. Ads list validation
    if not ads:
        return False, "Ads list cannot be empty"

    # 3. Duplicate ad_id validation (explicit)
    seen_ids = set()
    for ad in ads:
        if ad.ad_id in seen_ids:
            return False, f"Duplicate ad_id detected: '{ad.ad_id}'"
        seen_ids.add(ad.ad_id)

    # 4. Per-ad validation
    for idx, ad in enumerate(ads):
        if ad.cost <= 0:
            return False, f"Ad[{idx}] cost must be greater than zero"

        if ad.conversions > ad.clicks:
            return False, f"Ad[{idx}] conversions cannot exceed clicks"

    # 5. Budget feasibility check
    if min(ad.cost for ad in ads) > total_budget:
        return False, "Budget too low to select any ad"

    return True, None
