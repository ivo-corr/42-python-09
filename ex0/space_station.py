from pydantic import BaseModel, Field
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: str = Field(max_length=200)


def main():
    print("Space Station Data Validation")
    print("======================================")
    st = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance="2026-07-04T12:34:56+02:00",
        notes="Yes hello"
    )
    print("Valid station created:")
    print(f"ID: {st.station_id}")
    print(f"Name: {st.name}")
    print(f"Crew: {st.crew_size} people")
    print(f"Power: {st.power_level}%")
    print(f"Oxygen: {st.oxygen_level}%")
    print("Status:", "Operational\n" if
          st.is_operational else "Not operational\n")
    print("======================================")
    print("Expected validation error:")
    try:
        stt = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=22,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance="2026-07-04T12:34:56+02:00",
            notes="Yes hello"
        )
        _ = stt
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
