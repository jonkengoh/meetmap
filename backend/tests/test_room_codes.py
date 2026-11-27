
from app.rooms.codes import generate_room_code, ROOM_CODE_ALPHABET


def test_room_code_has_six_characters():
    code = generate_room_code()

    assert len(code) == 6


def test_room_code_uses_valid_characters():
    code = generate_room_code()

    assert all(char in ROOM_CODE_ALPHABET for char in code)


def test_room_code_excludes_ambiguous_characters():
    code = generate_room_code()

    assert not any(char in "01OI" for char in code)


def test_room_codes_are_not_always_identical():
    codes = {generate_room_code() for _ in range(20)}

    assert len(codes) > 1
