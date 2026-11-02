from copy import deepcopy

from fastapi import APIRouter, HTTPException
from sqlalchemy import delete, select

from app.database import SessionLocal
from app.models.simulation import Recommendation, Scenario, SimulationRun
from app.schemas.simulation import (
    ResetRequest,
    ScenarioResponse,
    TriggerRequest,
)

router = APIRouter(
    prefix="/api/v1/simulations",
    tags=["Simulations"],
)


@router.get("/scenarios", response_model=list[ScenarioResponse])
def get_scenarios():
    with SessionLocal() as session:
        scenarios = session.scalars(
            select(Scenario).order_by(Scenario.id)
        ).all()

        return scenarios


@router.post("/trigger")
def trigger_simulation(request: TriggerRequest):
    with SessionLocal() as session:
        scenario = session.get(Scenario, request.scenario_id)

        if scenario is None:
            raise HTTPException(status_code=404, detail="Scenario not found")

        state = deepcopy(scenario.current_state or scenario.initial_state or {})
        generated_recommendations = []

        for station in state.get("stations", []):
            station_id = station.get("station_id", "unknown")

            for connector in station.get("connectors", []):
                connector_id = connector.get("connector_id", "unknown")
                status = connector.get("status", "unknown")

                if status == "available":
                    connector["status"] = "occupied"
                    status = "occupied"

                if status == "faulted":
                    message = (
                        f"Inspect connector {connector_id} "
                        f"at station {station_id}."
                    )
                    priority = "high"
                elif status == "occupied":
                    message = (
                        f"Monitor demand at station {station_id}: "
                        f"connector {connector_id} is occupied."
                    )
                    priority = "normal"
                else:
                    continue

                recommendation = Recommendation(
                    scenario_id=scenario.id,
                    message=message,
                    priority=priority,
                )
                session.add(recommendation)

                generated_recommendations.append(
                    {
                        "message": message,
                        "priority": priority,
                    }
                )

        scenario.current_state = state

        run = SimulationRun(
            scenario_id=scenario.id,
            status="completed",
            result=state,
        )
        session.add(run)
        session.commit()
        session.refresh(run)

        return {
            "message": "Simulation completed",
            "scenario_id": scenario.id,
            "run_id": run.id,
            "result": state,
            "recommendations": generated_recommendations,
        }


@router.get("/{scenario_id}", response_model=ScenarioResponse)
def get_simulation_state(scenario_id: int):
    with SessionLocal() as session:
        scenario = session.get(Scenario, scenario_id)

        if scenario is None:
            raise HTTPException(status_code=404, detail="Scenario not found")

        return scenario


@router.post("/reset")
def reset_simulation(request: ResetRequest):
    with SessionLocal() as session:
        scenario = session.get(Scenario, request.scenario_id)

        if scenario is None:
            raise HTTPException(status_code=404, detail="Scenario not found")

        scenario.current_state = deepcopy(scenario.initial_state)

        session.execute(
            delete(Recommendation).where(
                Recommendation.scenario_id == scenario.id
            )
        )

        reset_run = SimulationRun(
            scenario_id=scenario.id,
            status="reset",
            result=scenario.current_state,
        )
        session.add(reset_run)
        session.commit()

        return {
            "message": "Simulation reset to its initial state",
            "scenario_id": scenario.id,
            "current_state": scenario.current_state,
        }