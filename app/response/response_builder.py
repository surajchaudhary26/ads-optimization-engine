def build_success_response(selected_ads, total_cost):
    return {
        "success": True,
        "selected_ads": selected_ads,
        "total_cost": total_cost
    }


def build_error_response(error_message):
    return {
        "success": False,
        "error": error_message
    }
