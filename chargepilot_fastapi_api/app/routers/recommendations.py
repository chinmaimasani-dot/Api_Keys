from fastapi import APIRouter
from sqlalchemy import select

from app.database import SessionLocal
from app.models.simulation import Recommendation
from app.schemas.simulation import RecommendationResponse

router = APIRouter(
    prefix="/api/v1/recommendations",
    tags=["Recommendations"],
)


@router.get("", response_model=list[RecommendationResponse])
def get_recommendations(scenario_id: int | None = None):
    query = select(Recommendation).order_by(Recommendation.id.desc())

    if scenario_id is not None:
        query = query.where(Recommendation.scenario_id == scenario_id)

    with SessionLocal() as session:
        recommendations = session.scalars(query).all()
        return recommendations
    