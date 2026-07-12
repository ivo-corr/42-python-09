from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from enum import Enum


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str = Field(default="", max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def checks(self) -> "AlienContact":
        if (not self.contact_id.startswith("AC")):
            raise Exception("Contact ID must start with 'AC'")
        if ((self.contact_type is ContactType.PHYSICAL and
             not self.is_verified)):
            raise Exception("Physical contact has to be validated")
        if ((self.contact_type is ContactType.TELEPATHIC and
                self.witness_count < 3)):
            raise Exception("Telepathic contact requires at least 3 witnesses")
        if ((self.signal_strength > 7.0 and self.message_received == "")):
            raise Exception("Signals of strength 7 or above"
                            " must include received messages")
        return (self)


def main() -> None:
    try:
        ac = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.fromisoformat("2026-07-04T12:34:56+02:00"),
            contact_type=ContactType.RADIO,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli"
        )
    except Exception as e:
        print(e)
        exit(1)
    print("Alien Contact Log Validation")
    print("=======================================")
    print("Valid contact report:")
    print(f"ID: {ac.contact_id}")
    print(f"Type: {ac.contact_type}")
    print(f"Location: {ac.location}")
    print(f"Signal: {ac.signal_strength}/10")
    print(f"Duration: {ac.duration_minutes}")
    print(f"Witnesses: {ac.witness_count}")
    print(f"Message: {ac.message_received}")
    print("\n=======================================")
    print("Expected validation error:")
    try:
        ac = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.fromisoformat("2026-07-04T12:34:56+02:00"),
            contact_type=ContactType.TELEPATHIC,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=1,
            message_received="Greetings from Zeta Reticuli"
        )
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
