from sqlalchemy import select

from app.database import SessionLocal
from app.models.simulation import Scenario


sample_scenarios = [
    {
        "name": "Peak Demand",
        "description": "Simulate a busy charging station.",
        "state": {
            "stations": [
                {
                    "station_id": "ST-001",
                    "connectors": [
                        {"connector_id": "C1", "status": "occupied"},
                        {"connector_id": "C2", "status": "available"},
                    ],
                }
            ]
        },
    },
    {
        "name": "Connector Fault",
        "description": "Simulate a connector becoming unavailable.",
        "state": {
            "stations": [
                {
                    "station_id": "ST-002",
                    "connectors": [
                        {"connector_id": "C1", "status": "faulted"},
                    ],
                }
            ]
        },
    },
]


def seed_scenarios():
    with SessionLocal() as session:
        existing_names = set(session.scalars(select(Scenario.name)).all())
        added_names = []

        for item in sample_scenarios:
            if item["name"] in existing_names:
                continue

            scenario = Scenario(
                name=item["name"],
                description=item["description"],
                initial_state=item["state"],
                current_state=item["state"],
            )
            session.add(scenario)
            added_names.append(item["name"])

        session.commit()

        if added_names:
            print(f"Added scenarios: {', '.join(added_names)}")
        else:
            print("Both sample scenarios already exist.")


if __name__ == "__main__":
    seed_scenarios()