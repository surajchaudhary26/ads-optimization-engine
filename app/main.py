from fastapi import FastAPI
from app.api.schemas import HealthResponse
from app.api.endpoints import router as ads_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Ads Optimization Engine",
    description="Inference API for ad selection under budget constraints",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ads-optimization-ui-streamlit.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ads_router)


@app.get(
    "/",
    response_model=HealthResponse,
    summary="Health check",
    description="Verifies that the Ads Optimization Engine is running",
    response_description="Service health status"
)
def health_check():
    return HealthResponse(
        status="ok",
        service="ads-optimization-engine",
        message="Service is healthy and running"
    )
