from app.validation.input_validator import validate_input
from app.optimizers.optimizer_v1 import select_ads_rule_based
from app.optimizers.optimizer_v2 import optimize_ads_v2

from app.response.response_builder import (
    build_success_response,
    build_error_response
)

USE_ML_OPTIMIZER = True  # switch here


def decide_ads(ads, total_budget):
    # Validate input
    is_valid, error_message = validate_input(ads, total_budget)

    if not is_valid:
        return build_error_response(error_message)

    # Choose optimizer
    if USE_ML_OPTIMIZER:
        selected_ads = optimize_ads_v2(ads)
        total_cost = sum(ad["cost"] for ad in selected_ads)
    else:
        selected_ads, total_cost = select_ads_rule_based(
            ads, total_budget
        )
    return build_success_response(selected_ads, total_cost)
