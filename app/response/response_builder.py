from datetime import datetime
from typing import Dict, Any


def build_success_response(
    selected_ads,
    total_cost,
    total_budget,
    strategy
) -> Dict[str, Any]:

    return {
        "success": True,
        "strategy": strategy,
        "selected_ads": selected_ads,
        "total_cost": round(total_cost, 2),
        "remaining_budget": round(total_budget - total_cost, 2),
        "timestamp": datetime.utcnow().isoformat()
    }


def build_error_response(error_message: str) -> Dict[str, Any]:
    return {
        "success": False,
        "error": error_message,
        "timestamp": datetime.utcnow().isoformat()
    }
