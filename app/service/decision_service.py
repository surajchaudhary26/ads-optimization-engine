from typing import List, Dict
from app.api.schemas import AdInput
from app.validation.input_validator import validate_input
from app.optimizers.optimizer_v1 import select_ads_rule_based
from app.optimizers.optimizer_v2 import optimize_ads_v2
from app.response.response_builder import (
    build_success_response,
    build_error_response
)

USE_ML_OPTIMIZER = True  # switch strategy here


def decide_ads(
    ads: List[AdInput],
    total_budget: float
) -> Dict:

    is_valid, error = validate_input(ads, total_budget)
    if not is_valid:
        return build_error_response(error)

    if USE_ML_OPTIMIZER:
        result = optimize_ads_v2(ads, total_budget)
    else:
        result = select_ads_rule_based(ads, total_budget)

    return build_success_response(
        selected_ads=result["selected_ads"],
        total_cost=result["total_cost"],
        total_budget=total_budget,
        strategy=result["strategy"]
    )
