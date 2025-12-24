from typing import List, Tuple
from app.api.schemas import AdInput


def validate_input(
    ads: List[AdInput],
    total_budget: float
) -> Tuple[bool, str | None]:

    if total_budget <= 0:
        return False, "Total budget must be greater than zero"

    if not ads:
        return False, "Ads list cannot be empty"

    for idx, ad in enumerate(ads):
        if ad.cost <= 0:
            return False, f"Ad[{idx}] cost must be greater than zero"

        if ad.conversions > ad.clicks:
            return False, f"Ad[{idx}] conversions cannot exceed clicks"

    if min(ad.cost for ad in ads) > total_budget:
        return False, "Budget too low to select any ad"

    return True, None
