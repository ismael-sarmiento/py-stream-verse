# services/auth_service/tests/test_auth.py
import pytest
from fastapi.testclient import TestClient

from common.database import engine, SessionLocal
from common.models import Base
from services.auth_service.app import app  # tu FastAPI instance

# Datos de prueba
TEST_USER = {"username": "alice", "email": "alice@example.com", "password": "secret", "role": "client"}


@pytest.fixture(autouse=True)
def setup_db():
    # Crea todas las tablas en SQLite (o la DB que uses para tests)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


def test_register_and_login_and_protected_routes(client):
    # 1. Registrar usuario
    resp = client.post("/auth/register", json=TEST_USER)
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == TEST_USER["email"]
    assert "id" in data and "role" in data

    # 2. Intentar acceder a /auth/me sin token
    resp = client.get("/auth/me")
    assert resp.status_code == 401  # Unauthorized

    # 3. Hacer login
    resp = client.post("/auth/login", json=TEST_USER)
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    assert token

    headers = {"Authorization": f"Bearer {token}"}

    # 4. Acceder a /auth/me con token válido
    resp = client.get("/auth/me", headers=headers)
    assert resp.status_code == 200
    me = resp.json()
    assert me["email"] == TEST_USER["email"]

    # 5. Intentar /auth/users (admin-only) con rol client
    resp = client.get("/auth/users", headers=headers)
    assert resp.status_code == 403  # Forbidden

    # 6. Crear un admin directamente en la DB
    db = SessionLocal()
    from common.models import User, RoleEnum
    admin = User(
        username="admin",
        email="admin@example.com",
        password_hash="secret",
        role=RoleEnum.admin.value
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    db.close()

    # 7. Login con admin
    resp = client.post("/auth/login", json={
        "username": "admin",
        "email": "admin@example.com",
        "password": "secret",
        "role": "admin"}
                       )
    admin_token = resp.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 8. Acceder a /auth/users como admin
    resp = client.get("/auth/users", headers=admin_headers)
    assert resp.status_code == 200
    users = resp.json()
    assert isinstance(users, list)
    assert any(u["email"] == TEST_USER["email"] for u in users)
