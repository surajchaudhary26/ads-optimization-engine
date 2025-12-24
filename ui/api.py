import requests
from ui.config import BACKEND_DECIDE_ADS_URL


def call_decide_ads(payload: dict) -> dict:
    response = requests.post(
        BACKEND_DECIDE_ADS_URL,
        json=payload,
        timeout=15
    )
    response.raise_for_status()
    return response.json()
