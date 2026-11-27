
import pytest
from pydantic import ValidationError

from app.rooms.schemas import RoomCreateRequest, RoomStatus, RoomType


def test_temporary_room_defaults_to_24_hours():
    room = RoomCreateRequest(room_type=RoomType.TEMPORARY)

    assert room.duration_hours == 24


def test_room_name_is_optional():
    room = RoomCreateRequest()

    assert room.name is None


def test_room_name_is_trimmed():
    room = RoomCreateRequest(name="  Friday Dinner  ")

    assert room.name == "Friday Dinner"


def test_blank_room_name_becomes_none():
    room = RoomCreateRequest(name="   ")

    assert room.name is None


def test_temporary_room_accepts_custom_duration():
    room = RoomCreateRequest(
        room_type=RoomType.TEMPORARY,
        duration_hours=48,
    )

    assert room.duration_hours == 48


@pytest.mark.parametrize("duration", [0, 169, -1])
def test_temporary_room_rejects_invalid_duration(duration):
    with pytest.raises(ValidationError):
        RoomCreateRequest(
            room_type=RoomType.TEMPORARY,
            duration_hours=duration,
        )


def test_persistent_room_has_no_expiry_duration():
    room = RoomCreateRequest(
        room_type=RoomType.PERSISTENT,
    )

    assert room.duration_hours is None


def test_persistent_room_rejects_expiry_duration():
    with pytest.raises(ValidationError):
        RoomCreateRequest(
            room_type=RoomType.PERSISTENT,
            duration_hours=24,
        )


def test_room_status_values():
    assert RoomStatus.ACTIVE == "active"
    assert RoomStatus.EXPIRED == "expired"
    assert RoomStatus.CLOSED == "closed"
