from pydantic import BaseModel, Field
from typing import List
from pydantic import BaseModel, Field


class AdInput(BaseModel):
    ad_id: str = Field(..., description="Unique ad identifier", example="ad_201")
    cost: float = Field(..., gt=0, description="Cost of the ad", example=100)
    priority: int = Field(..., ge=1, le=3, description="Business priority (1–3)", example=3)
    clicks: int = Field(..., ge=0, description="Number of clicks", example=120)
    conversions: int = Field(..., ge=0, description="Number of conversions", example=12)


class AdsRequest(BaseModel):
    total_budget: float = Field(..., gt=0, description="Total available budget", example=500)
    ads: List[AdInput] = Field(..., min_items=1)

class HealthResponse(BaseModel):
    status: str = Field(example="ok")
    service: str = Field(example="ads-optimization-engine")
    message: str = Field(example="Service is healthy and running")


class SelectedAd(BaseModel):
    ad_id: str = Field(example="ad_101")
    cost: float = Field(example=50)
    priority: int = Field(example=2)
    ml_score: float = Field(example=12.5)
    final_score: float = Field(example=8.3)


class AdsDecisionResponse(BaseModel):
    success: bool = Field(example=True)
    strategy: str = Field(example="hybrid_ml")
    selected_ads: List[SelectedAd]
    total_cost: float = Field(example=230)
    remaining_budget: float = Field(example=70)
    timestamp: str = Field(example="2025-12-24T10:30:00")
