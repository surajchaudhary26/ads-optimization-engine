from fastapi import FastAPI 
from app.api.endpoints import router as ads_router

app = FastAPI(
    title="Ads Optimization Engine",
    description="Inference API for ad selection under budget constraints",
    version="1.0.0"
)

app.include_router(ads_router)

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "Ads Optimization Engine is running"
    }
