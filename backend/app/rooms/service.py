import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.participants.models import Participant
from app.rooms.codes import generate_room_code
from app.rooms.models import Room
from app.rooms.schemas import RoomCreateRequest, RoomStatus, RoomType


def create_room(
    db: Session,
    request: RoomCreateRequest,
) -> tuple[Room, Participant, str]:

    room_code = generate_room_code()

    while db.query(Room).filter_by(room_code=room_code).first():
        room_code = generate_room_code()

    session_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(
        session_token.encode()
    ).hexdigest()

    now = datetime.now(timezone.utc)

    expires_at = None

    if request.room_type == RoomType.TEMPORARY:
        duration_hours = request.duration_hours or 24
        expires_at = now + timedelta(hours=duration_hours)

    room = Room(
        room_code=room_code,
        name=request.name,
        room_type=request.room_type,
        status=RoomStatus.ACTIVE,
        created_at=now,
        expires_at=expires_at,
    )

    db.add(room)
    db.flush()

    participant = Participant(
        room_id=room.id,
        display_name="Host",
        session_token_hash=token_hash,
        is_owner=True,
        joined_at=now,
        last_seen_at=now,
    )

    db.add(participant)

    db.commit()

    db.refresh(room)
    db.refresh(participant)

    return room, participant, session_token