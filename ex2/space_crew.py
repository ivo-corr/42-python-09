from enum import Enum
from pydantic import BaseModel, Field, model_validator
from datetime import datetime


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_million: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check(self) -> "SpaceMission":
        if (not self.mission_id.startswith('M')):
            raise Exception("Mission ID must start with 'M'")
        if (not all([m.is_active for m in self.crew])):
            raise Exception("All crew members must be active")
        if (not (Rank.COMMANDER in [m.rank for m in self.crew]) and
                not (Rank.CAPTAIN in [m.rank for m in self.crew])):
            raise Exception("Mission must have at least "
                            "one Commander or Captain")
        if (self.duration_days > 365 and
                ((len([m for m in self.crew
                       if m.years_experience >= 5])/len(self.crew)) < 0.5)):
            raise Exception("Missions longer than 365 days require that "
                            "at least half the crew have 5 years or more "
                            "of experience")
        return (self)


def main() -> None:
    sm = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime.fromisoformat("2026-07-04T12:34:56+02:00"),
        duration_days=900,
        crew=[CrewMember(
            member_id="A00",
            name="Sarah Connor",
            rank=Rank.COMMANDER,
            age=36,
            specialization="Mission Command",
            years_experience=15
        ),
            CrewMember(
                member_id="A01",
                name="John Smith",
                rank=Rank.LIEUTENANT,
                age=27,
                specialization="Navigation",
                years_experience=7
        ),
            CrewMember(
                member_id="A02",
                name="Alice Johnson",
                rank=Rank.OFFICER,
                age=24,
                specialization="Engineering",
                years_experience=6
        )],
        budget_million=2500
    )
    print("Space Mission Crew Validation")
    print("=====================================")
    print("Valid mission created:")
    print(f"Mission: {sm.mission_name}")
    print(f"ID: {sm.mission_id}")
    print(f"Destination: {sm.destination}")
    print(f"Duration: {sm.duration_days} days")
    print(f"Budget: {sm.budget_million}")
    print(f"Crew size: {len(sm.crew)}")
    print("Crew member:")
    for m in sm.crew:
        print(f"- {m.name} ({m.rank}) - {m.specialization}")
    print("=====================================")
    print("Expected validation error:")
    try:
        sm_two = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.fromisoformat("2026-07-04T12:34:56+02:00"),
            duration_days=900,
            crew=[CrewMember(
                member_id="A00",
                name="Sarah Connor",
                rank=Rank.OFFICER,
                age=36,
                specialization="Mission Command",
                years_experience=15
            ),
                CrewMember(
                    member_id="A01",
                    name="John Smith",
                    rank=Rank.LIEUTENANT,
                    age=27,
                    specialization="Navigation",
                    years_experience=6
            ),
                CrewMember(
                    member_id="A02",
                    name="Alice Johnson",
                    rank=Rank.OFFICER,
                    age=24,
                    specialization="Engineering",
                    years_experience=7
            )],
            budget_million=2500
        )
        _ = sm_two
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
