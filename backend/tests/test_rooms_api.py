import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.dependencies import get_db
from app.main import app

from app.rooms.models import Room
from app.participants.models import Participant


@pytest.fixture
def testing_session_factory():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    factory = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    yield factory

    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    

@pytest.fixture
def client(testing_session_factory):
    def override_get_db():
        with testing_session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_create_room_endpoint(client):
    response = client.post("/rooms", json={})

    assert response.status_code == 201

    data = response.json()

    assert len(data["room_code"]) == 6
    assert data["room_type"] == "temporary"
    assert data["status"] == "active"
    assert data["expires_at"] is not None

    assert data["participant_id"] is not None
    assert data["display_name"] == "Host"
    assert data["session_token"] is not None


def test_create_persistent_room_endpoint(client):
    response = client.post(
        "/rooms",
        json={"room_type": "persistent"},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["room_type"] == "persistent"
    assert data["expires_at"] is None


def test_create_named_room_endpoint(client):
    response = client.post(
        "/rooms",
        json={"name": "Friday Dinner"},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Friday Dinner"


def test_create_room_with_custom_duration(client):
    response = client.post(
        "/rooms",
        json={
            "room_type": "temporary",
            "duration_hours": 48,
        },
    )

    assert response.status_code == 201


def test_invalid_room_duration_returns_422(client):
    response = client.post(
        "/rooms",
        json={
            "room_type": "temporary",
            "duration_hours": 169,
        },
    )

    assert response.status_code == 422


def test_persistent_room_rejects_duration(client):
    response = client.post(
        "/rooms",
        json={
            "room_type": "persistent",
            "duration_hours": 24,
        },
    )

    assert response.status_code == 422


def test_room_and_participant_are_stored(
    client,
    testing_session_factory,
):
    response = client.post("/rooms", json={})

    assert response.status_code == 201

    data = response.json()

    with testing_session_factory() as db:
        room = db.query(Room).filter_by(
            room_code=data["room_code"]
        ).first()

        participant = db.query(Participant).filter_by(
            id=data["participant_id"]
        ).first()

        assert room is not None
        assert participant is not None
        assert participant.is_owner is True