from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class ContactType(Enum):
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
    def checks(self):
        if (not self.contact_id.startswith("AC") or
            (self.contact_type is ContactType.PHYSICAL and
             not self.is_verified) or
                (self.contact_type is ContactType.TELEPATHIC and
                    self.witness_count < 3) or
                (self.signal_strength > 7.0 and self.message_receive != "")):
            print("WRONG")
