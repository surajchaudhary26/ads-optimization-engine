from datetime import datetime
from typing import Dict, Any, List


def build_success_response(
    selected_ads: List[Dict[str, Any]],
    total_cost: float,
    total_budget: float,
    strategy: str
) -> Dict[str, Any]:
    """
    Builds a standardized success response for the API.
    This is the single source of truth for response formatting.
    """

    return {
        "success": True,
        "strategy": strategy,
        "selected_ads": selected_ads,
        "total_cost": round(float(total_cost), 2),
        "remaining_budget": round(float(total_budget - total_cost), 2),
        "timestamp": datetime.utcnow().isoformat()
    }


def build_error_response(error_message: str) -> Dict[str, Any]:
    """
    Builds a standardized error response for the API.
    """

    return {
        "success": False,
        "error": error_message,
        "timestamp": datetime.utcnow().isoformat()
    }
