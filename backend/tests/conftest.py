import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app
from database import Base, get_db
from models import ChatSession, Document, Message

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with database dependency override."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_session(db):
    """Create a sample chat session."""
    session = ChatSession(title="Test Session")
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@pytest.fixture
def sample_document(db):
    """Create a sample document."""
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
    return document


@pytest.fixture
def sample_messages(db, sample_session):
    """Create sample messages for a session."""
    messages = [
        Message(session_id=sample_session.id, role="user", content="Hello"),
        Message(session_id=sample_session.id, role="assistant", content="Hi there!")
    ]
    for msg in messages:
        db.add(msg)
    db.commit()
    return messages
