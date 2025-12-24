from fastapi import APIRouter, HTTPException, status
from app.api.schemas import AdsRequest, AdsDecisionResponse
from app.service.decision_service import decide_ads

router = APIRouter()


@router.post(
    "/decide-ads",
    response_model=AdsDecisionResponse,
    status_code=status.HTTP_200_OK,
    summary="Decide optimal ads under a given budget"
)
def decide_ads_endpoint(request: AdsRequest):
    result = decide_ads(request.ads, request.total_budget)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )

    return result
