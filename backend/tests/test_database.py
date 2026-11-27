from app.database import Base, engine


def test_database_engine_uses_sqlite():
    assert engine.dialect.name == "sqlite"


def test_base_metadata_is_available():
    assert Base.metadata is not None