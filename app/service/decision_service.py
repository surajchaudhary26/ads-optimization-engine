from app.validation.input_validator import validate_input
from app.optimizers.optimizer_v1 import select_ads_rule_based


def decide_ads(ads, total_budget):
    # Step 1: Validate input
    is_valid, error_message = validate_input(ads, total_budget)

    if not is_valid:
        return {
            "success": False,
            "error": error_message
        }

    # Step 2: Apply selection logic
    selected_ads, total_cost = select_ads_rule_based(ads, total_budget)

    # Step 3: Return response
    return {
        "success": True,
        "selected_ads": selected_ads,
        "total_cost": total_cost
    }
