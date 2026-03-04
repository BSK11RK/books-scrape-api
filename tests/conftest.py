import os, pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from backend.main import app
from backend.database import Base, get_db

# テスト用SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture()
def client():
    os.environ["ENV"] = "test"
    return TestClient(app)

@pytest.fixture
def admin_token(client):
    client.post("/register", params={"username": "admin", "password": "admin123"})
    res = client.post(
        "/login",
        data={"username": "admin", "password": "admin123"},
        headers={"Context-Type": "application/x-www-form-urlencoded"},
    )
    return res.json()["access_token"]