from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ScenarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    initial_state: dict[str, Any]
    current_state: dict[str, Any]
    created_at: datetime


class TriggerRequest(BaseModel):
    scenario_id: int


class ResetRequest(BaseModel):
    scenario_id: int


class SimulationRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scenario_id: int
    status: str
    result: dict[str, Any]
    created_at: datetime


class RecommendationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scenario_id: int
    message: str
    priority: str
    created_at: datetime