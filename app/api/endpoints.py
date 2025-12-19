from fastapi import APIRouter, HTTPException
from app.service.decision_service import decide_ads

router = APIRouter()


@router.post("/decide-ads")
def decide_ads_endpoint(request: dict):
    """
    API endpoint to decide which ads to select under a given budget.
    """

    ads = request.get("ads")
    total_budget = request.get("total_budget")

    result = decide_ads(ads, total_budget)

    # If validation fails
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])

    return result
