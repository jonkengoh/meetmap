
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator


class RoomType(str, Enum):
    TEMPORARY = "temporary"
    PERSISTENT = "persistent"


class RoomStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CLOSED = "closed"


class RoomCreateRequest(BaseModel):
    name: str | None = Field(default=None, max_length=80)
    room_type: RoomType = RoomType.TEMPORARY
    duration_hours: int | None = Field(default=None, ge=1, le=168)

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        return value or None

    @model_validator(mode="after")
    def validate_duration(self):
        if self.room_type == RoomType.TEMPORARY:
            if self.duration_hours is None:
                self.duration_hours = 24

        elif self.duration_hours is not None:
            raise ValueError(
                "Persistent rooms cannot have an expiry duration."
            )

        return self

class RoomCreateResponse(BaseModel):
    room_id: str
    room_code: str
    name: str | None
    room_type: RoomType
    status: RoomStatus
    created_at: datetime
    expires_at: datetime | None

    participant_id: str
    display_name: str
    session_token: str