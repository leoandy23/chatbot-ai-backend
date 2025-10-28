from fastapi.testclient import TestClient
from main import app
from uuid import UUID, uuid4

client = TestClient(app)


def test_register_user():
    email = f"user_{uuid4()}@example.com"
    username = f"user_{uuid4()}"
    response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "secure123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "User registered successfully"
    assert "user_id" in data
    assert isinstance(UUID(str(data["user_id"])), UUID)


def test_login_user():
    response = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "secure123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_user():
    response = client.post(
        "/api/auth/login",
        json={
            "username": "nonexistentuser",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Invalid username or password"


def test_register_existing_user():
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "secure123",
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Username or email already exists"
