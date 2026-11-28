from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.rooms.schemas import RoomCreateRequest, RoomCreateResponse
from app.rooms.service import create_room


router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
)


@router.post(
    "",
    response_model=RoomCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_room_endpoint(
    request: RoomCreateRequest,
    db: Session = Depends(get_db),
):
    room, participant, session_token = create_room(db, request)

    return RoomCreateResponse(
        room_id=room.id,
        room_code=room.room_code,
        name=room.name,
        room_type=room.room_type,
        status=room.status,
        created_at=room.created_at,
        expires_at=room.expires_at,
        participant_id=participant.id,
        display_name=participant.display_name,
        session_token=session_token,
    )