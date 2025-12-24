from pydantic import BaseModel, Field
from typing import List


class AdInput(BaseModel):
    ad_id: str = Field(..., example="ad_101")
    cost: float = Field(..., gt=0, example=100)
    priority: int = Field(..., ge=1, le=3, example=3)
    clicks: int = Field(..., ge=0, example=120)
    conversions: int = Field(..., ge=0, example=12)


class AdsRequest(BaseModel):
    total_budget: float = Field(..., gt=0, example=500)
    ads: List[AdInput]


class AdsDecisionResponse(BaseModel):
    success: bool
    strategy: str
    selected_ads: list
    total_cost: float
    remaining_budget: float
    timestamp: str


class HealthResponse(BaseModel):
    status: str = Field(example="ok")
    service: str = Field(example="ads-optimization-engine")
    message: str = Field(example="Service is healthy and running")
