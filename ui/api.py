import requests
from typing import Dict, Any
from config import DECIDE_ENDPOINT

def decide_ads(payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(
        DECIDE_ENDPOINT,
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    return response.json()
