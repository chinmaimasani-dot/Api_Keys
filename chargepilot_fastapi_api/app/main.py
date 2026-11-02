from fastapi import FastAPI

from app.routers import recommendations, simulations

app = FastAPI(
    title="ChargePilot Simulation API",
    version="1.0.0",
    description="Simulation and recommendations API for EV charging stations.",
)

app.include_router(simulations.router)
app.include_router(recommendations.router)


@app.get("/api/v1/health", tags=["Health"])
def health_check():
    return {
        "status": "success",
        "message": "API is running",
    }