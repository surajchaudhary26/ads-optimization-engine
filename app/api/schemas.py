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
