from pydantic import BaseModel, Field
from typing import List


class AdInput(BaseModel):
    ad_id: str = Field(..., example="ad_201")
    cost: float = Field(..., gt=0,example=100)
    priority: int = Field(..., example=3)
    clicks: int = Field(..., ge=0, example=120)
    conversions: int = Field(..., gt=0, example=12)


class AdsRequest(BaseModel):
    total_budget: float = Field(..., example=500)
    ads: List[AdInput] = Field(
        ...,
        example=[
            {
                "ad_id": "ad_201",
                "cost": 100,
                "priority": 3,
                "clicks": 120,
                "conversions": 12
            },
            {
                "ad_id": "ad_202",
                "cost": 180,
                "priority": 2,
                "clicks": 90,
                "conversions": 6
            }
        ]
    )
