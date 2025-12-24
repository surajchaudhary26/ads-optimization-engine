from pydantic import BaseModel, Field
from typing import List


# =========================
# INPUT SCHEMAS
# =========================

class AdInput(BaseModel):
    ad_id: str = Field(
        ...,
        description="Unique ad identifier",
        example="ad_201"
    )
    cost: float = Field(
        ...,
        gt=0,
        description="Cost of the ad",
        example=100
    )
    priority: int = Field(
        ...,
        ge=1,
        le=3,
        description="Business priority (1–3)",
        example=3
    )
    clicks: int = Field(
        ...,
        ge=0,
        description="Number of clicks",
        example=120
    )
    conversions: int = Field(
        ...,
        ge=0,
        description="Number of conversions",
        example=12
    )


class AdsRequest(BaseModel):
    total_budget: float = Field(
        ...,
        gt=0,
        description="Total available budget",
        example=500
    )
    ads: List[AdInput] = Field(
        ...,
        min_items=1,
        description="List of ads to evaluate"
    )


# =========================
# HEALTH CHECK
# =========================

class HealthResponse(BaseModel):
    status: str = Field(example="ok")
    service: str = Field(example="ads-optimization-engine")
    message: str = Field(example="Service is healthy and running")


# =========================
# OUTPUT SCHEMAS
# =========================

class SelectedAd(BaseModel):
    ad_id: str = Field(
        description="Ad identifier",
        example="ad_101"
    )
    cost: float = Field(
        description="Cost of the ad",
        example=50
    )
    priority: int = Field(
        description="Business priority",
        example=2
    )
    ml_score: float = Field(
        description="Raw ML prediction score",
        example=12.5
    )
    final_score: float = Field(
        description="Final hybrid score after business logic",
        example=-3.39
    )
    rank: int = Field(
        description="Rank of the ad (1 = best)",
        example=1
    )
    label: str = Field(
        description="Human-readable label for the ad",
        example="Best Choice"
    )
    reason: str = Field(
        description="Human-readable explanation for ad selection",
        example="This ad ranks highest due to strong predicted performance and high business priority."
    )


class AdsDecisionResponse(BaseModel):
    success: bool = Field(example=True)
    strategy: str = Field(
        description="Optimization strategy used",
        example="hybrid_ml"
    )
    selected_ads: List[SelectedAd]
    total_cost: float = Field(
        description="Total budget used",
        example=230
    )
    remaining_budget: float = Field(
        description="Remaining unused budget",
        example=70
    )
    timestamp: str = Field(
        description="UTC timestamp of decision",
        example="2025-12-24T10:30:00"
    )
