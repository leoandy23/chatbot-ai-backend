from fastapi.testclient import TestClient
import pytest
from main import app
from uuid import UUID, uuid4

client = TestClient(app)


def test_list_conversations():
    response_login = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "secure123",
        },
    )
    assert response_login.status_code == 200
    data_login = response_login.json()
    assert "access_token" in data_login
    access_token = data_login["access_token"]
    response = client.get(
        "/api/conversation/list", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_conversations_unauthenticated():
    response = client.get("/api/conversation/list")
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Not authenticated"


def test_get_conversation_details():
    response_login = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "secure123",
        },
    )
    assert response_login.status_code == 200
    data_login = response_login.json()
    assert "access_token" in data_login
    access_token = data_login["access_token"]
    # First, list conversations to get a valid conversation ID
    response_list = client.get(
        "/api/conversation/list", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response_list.status_code == 200
    conversations = response_list.json()
    if not conversations:
        pytest.skip("No conversations available to test.")
    conversation_id = conversations[0]["id"]
    # Now, get details of the selected conversation
    response_detail = client.get(
        f"/api/conversation/{conversation_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response_detail.status_code == 200
    data_detail = response_detail.json()
    assert "id" in data_detail
    assert data_detail["id"] == conversation_id


def test_get_conversation_details_unauthenticated():
    response = client.get(f"/api/conversation/{uuid4()}")
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Not authenticated"


def test_get_conversation_details_not_found():
    response_login = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "secure123",
        },
    )
    assert response_login.status_code == 200
    data_login = response_login.json()
    assert "access_token" in data_login
    access_token = data_login["access_token"]
    invalid_conversation_id = str(uuid4())
    response = client.get(
        f"/api/conversation/{invalid_conversation_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Conversation not found"


def test_create_new_conversation():
    response_login = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "secure123",
        },
    )
    assert response_login.status_code == 200
    data_login = response_login.json()
    assert "access_token" in data_login
    access_token = data_login["access_token"]
    query = "What is the capital of France?"
    response = client.post(
        "/api/conversation/new",
        json={"query": query},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "title" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert "response" in data
    assert isinstance(data["response"], str)


def test_create_new_conversation_unauthenticated():
    query = "What is the capital of France?"
    response = client.post(
        "/api/conversation/new",
        json={"query": query},
    )
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Not authenticated"


def test_create_new_conversation_missing_query():
    response_login = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "secure123",
        },
    )
    assert response_login.status_code == 200
    data_login = response_login.json()
    assert "access_token" in data_login
    access_token = data_login["access_token"]
    response = client.post(
        "/api/conversation/new",
        json={},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_add_message_to_conversation():
    response_login = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "secure123",
        },
    )
    assert response_login.status_code == 200
    data_login = response_login.json()
    assert "access_token" in data_login
    access_token = data_login["access_token"]
    # First, create a new conversation to get a valid conversation ID
    query_initial = "What is the capital of France?"
    response_create = client.post(
        "/api/conversation/new",
        json={"query": query_initial},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response_create.status_code == 200
    data_create = response_create.json()
    conversation_id = data_create["id"]
    # Now, add a message to the created conversation
    query_new = "And what about Germany?"
    response_add = client.post(
        f"/api/conversation/{conversation_id}/message",
        json={"query": query_new},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response_add.status_code == 200
    data_add = response_add.json()
    assert "response" in data_add
    assert isinstance(data_add["response"], str)


def test_add_message_to_conversation_unauthenticated():
    conversation_id = str(uuid4())
    query_new = "And what about Germany?"
    response = client.post(
        f"/api/conversation/{conversation_id}/message",
        json={"query": query_new},
    )
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Not authenticated"


def test_add_message_to_conversation_not_found():
    response_login = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "secure123",
        },
    )
    assert response_login.status_code == 200
    data_login = response_login.json()
    assert "access_token" in data_login
    access_token = data_login["access_token"]
    invalid_conversation_id = str(uuid4())
    query_new = "And what about Germany?"
    response = client.post(
        f"/api/conversation/{invalid_conversation_id}/message",
        json={"query": query_new},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Conversation not found"


def test_change_title_of_conversation():
    response_login = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "secure123",
        },
    )
    assert response_login.status_code == 200
    data_login = response_login.json()
    assert "access_token" in data_login
    access_token = data_login["access_token"]
    # First, create a new conversation to get a valid conversation ID
    query_initial = "What is the capital of France?"
    response_create = client.post(
        "/api/conversation/new",
        json={"query": query_initial},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response_create.status_code == 200
    data_create = response_create.json()
    conversation_id = data_create["id"]
    # Now, change the title of the created conversation
    new_title = "Geography Questions"
    response_change = client.put(
        f"/api/conversation/{conversation_id}/title",
        json={"new_title": new_title},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response_change.status_code == 200
    data_change = response_change.json()
    assert "title" in data_change
    assert data_change["title"] == new_title


def test_change_title_of_conversation_unauthenticated():
    conversation_id = str(uuid4())
    new_title = "Geography Questions"
    response = client.put(
        f"/api/conversation/{conversation_id}/title",
        json={"new_title": new_title},
    )
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Not authenticated"


def test_change_title_of_conversation_not_found():
    response_login = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "secure123",
        },
    )
    assert response_login.status_code == 200
    data_login = response_login.json()
    assert "access_token" in data_login
    access_token = data_login["access_token"]
    invalid_conversation_id = str(uuid4())
    new_title = "Geography Questions"
    response = client.put(
        f"/api/conversation/{invalid_conversation_id}/title",
        json={"new_title": new_title},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Conversation not found"


def test_delete_conversation():
    response_login = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "secure123",
        },
    )
    assert response_login.status_code == 200
    data_login = response_login.json()
    assert "access_token" in data_login
    access_token = data_login["access_token"]
    # First, create a new conversation to get a valid conversation ID
    query_initial = "What is the capital of France?"
    response_create = client.post(
        "/api/conversation/new",
        json={"query": query_initial},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response_create.status_code == 200
    data_create = response_create.json()
    conversation_id = data_create["id"]
    # Now, delete the created conversation
    response_delete = client.delete(
        f"/api/conversation/{conversation_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response_delete.status_code == 200
    data_delete = response_delete.json()
    assert "message" in data_delete
    assert data_delete["message"] == "Conversation deleted successfully."
