import pytest
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import ChatSession, Document, Message


def test_chat_session_model(db):
    """Test ChatSession model."""
    session = ChatSession(title="Test Session")
    db.add(session)
    db.commit()
    db.refresh(session)
    
    assert session.id is not None
    assert session.title == "Test Session"
    assert isinstance(session.created_at, datetime)
    assert isinstance(session.updated_at, datetime)


def test_document_model(db):
    """Test Document model."""
    document = Document(
        filename="test.pdf",
        original_filename="test.pdf",
        mime_type="application/pdf",
        file_size=1024,
        gemini_uri="https://example.com/test.pdf",
        gemini_name="files/test"
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    
    assert document.id is not None
    assert document.filename == "test.pdf"
    assert document.is_active is True
    assert isinstance(document.uploaded_at, datetime)


def test_message_model(db, sample_session):
    """Test Message model."""
    message = Message(
        session_id=sample_session.id,
        role="user",
        content="Hello, world!"
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    assert message.id is not None
    assert message.session_id == sample_session.id
    assert message.role == "user"
    assert message.content == "Hello, world!"
    assert isinstance(message.created_at, datetime)


def test_session_messages_relationship(db, sample_session):
    """Test relationship between session and messages."""
    # Add messages
    msg1 = Message(session_id=sample_session.id, role="user", content="Question")
    msg2 = Message(session_id=sample_session.id, role="assistant", content="Answer")
    db.add_all([msg1, msg2])
    db.commit()
    
    # Refresh session to load relationships
    db.refresh(sample_session)
    
    assert len(sample_session.messages) == 2
    assert sample_session.messages[0].content == "Question"
    assert sample_session.messages[1].content == "Answer"


def test_cascade_delete_messages(db, sample_session):
    """Test that deleting a session cascades to messages."""
    # Add messages
    msg1 = Message(session_id=sample_session.id, role="user", content="Test")
    db.add(msg1)
    db.commit()
    
    # Delete session
    db.delete(sample_session)
    db.commit()
    
    # Verify messages are also deleted
    messages = db.query(Message).filter(Message.session_id == sample_session.id).all()
    assert len(messages) == 0
