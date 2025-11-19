import pytest
from models import ChatSession, Document, Message


def test_create_session(client):
    """Test creating a new chat session."""
    response = client.post("/api/sessions", json={"title": "My Test Session"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "My Test Session"
    assert "id" in data
    assert "created_at" in data


def test_create_session_without_title(client):
    """Test creating a session without title."""
    response = client.post("/api/sessions", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] is None


def test_list_sessions(client, sample_session):
    """Test listing all sessions."""
    response = client.get("/api/sessions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["id"] == sample_session.id


def test_get_session_messages(client, sample_session, sample_messages):
    """Test getting messages for a session."""
    response = client.get(f"/api/sessions/{sample_session.id}/messages")
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == sample_session.id
    assert data["total"] == 2
    assert len(data["messages"]) == 2


def test_get_session_messages_not_found(client):
    """Test getting messages for non-existent session."""
    response = client.get("/api/sessions/999/messages")
    assert response.status_code == 404


def test_list_documents(client, sample_document):
    """Test listing documents."""
    response = client.get("/api/documents")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["documents"]) >= 1


def test_list_documents_pagination(client, db):
    """Test document list pagination."""
    # Create multiple documents
    for i in range(5):
        doc = Document(
            filename=f"test{i}.pdf",
            original_filename=f"test{i}.pdf",
            mime_type="application/pdf",
            file_size=1024,
            gemini_uri=f"https://example.com/test{i}.pdf",
            gemini_name=f"files/test{i}"
        )
        db.add(doc)
    db.commit()
    
    # Test pagination
    response = client.get("/api/documents?skip=0&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data["documents"]) == 3
    assert data["total"] == 5


def test_delete_document(client, sample_document):
    """Test deleting a document."""
    response = client.delete(f"/api/documents/{sample_document.id}")
    assert response.status_code == 200
    
    # Verify it's marked as inactive
    response = client.get("/api/documents?active_only=false")
    data = response.json()
    doc = next((d for d in data["documents"] if d["id"] == sample_document.id), None)
    assert doc is not None
    assert doc["is_active"] is False


def test_delete_document_not_found(client):
    """Test deleting non-existent document."""
    response = client.delete("/api/documents/999")
    assert response.status_code == 404


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
