from app.rooms.models import Room
from app.rooms.schemas import RoomStatus, RoomType


def test_room_table_name():
    assert Room.__tablename__ == "rooms"


def test_room_has_expected_columns():
    expected_columns = {
        "id",
        "room_code",
        "name",
        "room_type",
        "status",
        "created_at",
        "expires_at",
    }

    actual_columns = set(Room.__table__.columns.keys())

    assert actual_columns == expected_columns


def test_room_code_is_unique():
    column = Room.__table__.columns["room_code"]

    assert column.unique is True
    assert column.nullable is False


def test_room_name_is_optional():
    column = Room.__table__.columns["name"]

    assert column.nullable is True


def test_room_expiry_is_optional():
    column = Room.__table__.columns["expires_at"]

    assert column.nullable is True


def test_room_status_default_is_active():
    column = Room.__table__.columns["status"]

    assert column.default.arg == RoomStatus.ACTIVE


def test_room_type_enum_values():
    column = Room.__table__.columns["room_type"]

    assert column.type.enums == [
        RoomType.TEMPORARY.value,
        RoomType.PERSISTENT.value,
    ]


def test_room_status_enum_values():
    column = Room.__table__.columns["status"]

    assert column.type.enums == [
        RoomStatus.ACTIVE.value,
        RoomStatus.EXPIRED.value,
        RoomStatus.CLOSED.value,
    ]