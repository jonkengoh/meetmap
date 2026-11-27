from app.participants.models import Participant


def test_participant_table_name():
    assert Participant.__tablename__ == "participants"


def test_participant_has_expected_columns():
    expected_columns = {
        "id",
        "room_id",
        "display_name",
        "session_token_hash",
        "is_owner",
        "joined_at",
        "last_seen_at",
    }

    actual_columns = set(Participant.__table__.columns.keys())

    assert actual_columns == expected_columns


def test_participant_room_id_is_foreign_key():
    column = Participant.__table__.columns["room_id"]

    assert len(column.foreign_keys) == 1

    foreign_key = next(iter(column.foreign_keys))

    assert foreign_key.target_fullname == "rooms.id"
    assert foreign_key.ondelete == "CASCADE"


def test_participant_room_id_is_indexed():
    column = Participant.__table__.columns["room_id"]

    assert column.index is True


def test_participant_display_name_is_required():
    column = Participant.__table__.columns["display_name"]

    assert column.nullable is False


def test_session_token_hash_is_unique():
    column = Participant.__table__.columns["session_token_hash"]

    assert column.unique is True
    assert column.nullable is False


def test_participant_owner_default_is_false():
    column = Participant.__table__.columns["is_owner"]

    assert column.default.arg is False


def test_participant_id_is_primary_key():
    column = Participant.__table__.columns["id"]

    assert column.primary_key is True