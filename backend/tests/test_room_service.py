import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.participants.models import Participant
from app.rooms.models import Room
from app.rooms.schemas import RoomCreateRequest, RoomType
from app.rooms.service import create_room


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    with TestingSessionLocal() as session:
        yield session

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_create_temporary_room(db):
    request = RoomCreateRequest()

    room, participant, token = create_room(db, request)

    assert room.room_code is not None
    assert len(room.room_code) == 6
    assert room.room_type == RoomType.TEMPORARY
    assert room.expires_at is not None

    assert participant.room_id == room.id
    assert participant.is_owner is True
    assert participant.display_name == "Host"

    assert token is not None
    assert participant.session_token_hash != token


def test_create_persistent_room(db):
    request = RoomCreateRequest(
        room_type=RoomType.PERSISTENT,
    )

    room, participant, token = create_room(db, request)

    assert room.room_type == RoomType.PERSISTENT
    assert room.expires_at is None
    assert participant.is_owner is True


def test_create_named_room(db):
    request = RoomCreateRequest(name="Friday Dinner")

    room, participant, token = create_room(db, request)

    assert room.name == "Friday Dinner"


def test_room_and_participant_are_persisted(db):
    request = RoomCreateRequest()

    room, participant, token = create_room(db, request)

    stored_room = db.query(Room).filter_by(
        id=room.id
    ).first()

    stored_participant = db.query(Participant).filter_by(
        id=participant.id
    ).first()

    assert stored_room is not None
    assert stored_participant is not None