from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.rooms.schemas import RoomStatus, RoomType


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    room_code: Mapped[str] = mapped_column(
        String(6),
        unique=True,
        nullable=False,
    )

    name: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True,
    )

    room_type: Mapped[RoomType] = mapped_column(
        Enum(
            RoomType,
            native_enum=False,
            values_callable=lambda enum: [item.value for item in enum],
        ),
        nullable=False,
    )

    status: Mapped[RoomStatus] = mapped_column(
        Enum(
            RoomStatus,
            native_enum=False,
            values_callable=lambda enum: [item.value for item in enum],
        ),
        nullable=False,
        default=RoomStatus.ACTIVE,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )