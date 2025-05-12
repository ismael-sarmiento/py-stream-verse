# services/auth-service/tests/test_models.py
import pytest
from sqlalchemy import create_engine, inspect

from common.database import DATABASE_URL_SQLITE
from common.models import Base  # ajusta import según tu paquete


@pytest.fixture
def engine():
    # Usamos SQLite en fichero temporal para test
    # fd, path = tempfile.mkstemp(suffix=".db")
    # os.close(fd)
    url = DATABASE_URL_SQLITE
    engine = create_engine(url)
    yield engine
    # os.remove(url.split("sqlite:///")[-1])


def test_models_create_tables(engine):
    # Crea todas las tablas definidas en Base.metadata
    Base.metadata.create_all(engine)

    insp = inspect(engine)
    tables = insp.get_table_names()
    # Comprueba que la tabla 'users' (y cualquier otra que definas) exista
    assert "users" in tables
    assert "movies" in tables
    assert "series" in tables
    assert "user_favorites" in tables
    assert "user_watched" in tables
