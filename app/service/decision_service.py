from typing import List, Dict, Any

from app.api.schemas import AdInput
from app.validation.input_validator import validate_input
from app.optimizers.optimizer_v1 import select_ads_rule_based
from app.optimizers.optimizer_v2 import optimize_ads_v2
from app.response.response_builder import (
    build_success_response,
    build_error_response
)
from app.service.reasoning import generate_reason

USE_ML_OPTIMIZER = True


def decide_ads(
    ads: List[AdInput],
    total_budget: float
) -> Dict[str, Any]:

    # 1. Validate input
    is_valid, error = validate_input(ads, total_budget)
    if not is_valid:
        return build_error_response(error)

    # 2. Run optimizer (DEBUG MODE)
    try:
        if USE_ML_OPTIMIZER:
            raw_result = optimize_ads_v2(ads, total_budget)
        else:
            raw_result = select_ads_rule_based(ads, total_budget)
    except Exception as exc:
        print("OPTIMIZER ERROR:", exc)
        raise  # 🔥 VERY IMPORTANT

    # 3. Contract validation
    required_keys = {"selected_ads", "total_cost", "strategy"}
    if not isinstance(raw_result, dict) or not required_keys.issubset(raw_result):
        return build_error_response("Invalid optimizer response format")

    # 4. Enrich ads
    enriched_ads = []
    for idx, ad in enumerate(raw_result["selected_ads"], start=1):
        explanation = generate_reason(ad, rank=idx)
        enriched_ads.append({
            **ad,
            "rank": explanation["rank"],
            "label": explanation["label"],
            "reason": explanation["reason"]
        })

    # 5. Response
    return build_success_response(
        selected_ads=enriched_ads,
        total_cost=raw_result["total_cost"],
        total_budget=total_budget,
        strategy=raw_result["strategy"]
    )
