from fastapi import FastAPI
from app.api.endpoints import router as ads_router
from app.api.schemas import HealthResponse

app = FastAPI(
    title="Ads Optimization Engine",
    description="API to select optimal ads under budget constraints",
    version="1.0.0"
)

app.include_router(ads_router, tags=["Ads Optimization"])


@app.get(
    "/",
    response_model=HealthResponse,
    summary="Health check",
    description="Verifies that the Ads Optimization Engine is running"
)
def health_check():
    return {
        "status": "ok",
        "service": "ads-optimization-engine",
        "message": "Service is healthy and running"
    }
