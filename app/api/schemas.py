from pydantic import BaseModel, Field
from typing import List


class AdInput(BaseModel):
    ad_id: str = Field(..., example="ad_201")
    cost: float = Field(..., example=100)
    priority: int = Field(..., example=4)
    clicks: int = Field(..., example=120)
    conversions: int = Field(..., example=12)


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
