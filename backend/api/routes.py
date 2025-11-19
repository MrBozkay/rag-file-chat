from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
from pathlib import Path

from gemini_client import gemini_client
from database import get_db
from models import ChatSession, Document, Message
from schemas import (
    ChatRequest, ChatResponse, ChatSessionCreate, ChatSessionResponse,
    DocumentUploadResponse, DocumentResponse, DocumentListResponse,
    MessageResponse, SessionMessagesResponse
)
from exceptions import (
    DocumentUploadError, GeminiAPIError, SessionNotFoundError,
    DocumentNotFoundError, FileSizeExceededError, InvalidFileTypeError
)
from config import settings
from logger import get_logger

router = APIRouter()
logger = get_logger("routes")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def validate_file(file: UploadFile) -> None:
    """Validate uploaded file size and type."""
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > settings.max_file_size:
        raise FileSizeExceededError(settings.max_file_size)
    
    # Check file type
    if file.content_type not in settings.allowed_file_types_list:
        raise InvalidFileTypeError(file.content_type, settings.allowed_file_types_list)


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a document to Gemini and save metadata to database."""
    try:
        logger.info(f"Uploading file: {file.filename}")
        
        # Validate file
        validate_file(file)
        
        # Save file temporarily
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file size
        file_size = Path(file_path).stat().st_size
        
        # Upload to Gemini
        gemini_file = gemini_client.upload_file(file_path, mime_type=file.content_type)
        
        # Save to database
        db_document = Document(
            filename=file.filename,
            original_filename=file.filename,
            mime_type=file.content_type,
            file_size=file_size,
            gemini_uri=gemini_file.uri,
            gemini_name=gemini_file.name
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        # Clean up local file
        os.remove(file_path)
        
        logger.info(f"Successfully uploaded file: {file.filename} (ID: {db_document.id})")
        
        return DocumentUploadResponse(
            id=db_document.id,
            filename=db_document.filename,
            original_filename=db_document.original_filename,
            mime_type=db_document.mime_type,
            file_size=db_document.file_size,
            gemini_uri=db_document.gemini_uri,
            gemini_name=db_document.gemini_name,
            uploaded_at=db_document.uploaded_at
        )
    except (FileSizeExceededError, InvalidFileTypeError):
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise DocumentUploadError(str(e))


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Send a chat message and get response from Gemini."""
    try:
        logger.info(f"Processing chat request for session: {request.session_id}")
        
        # Get or create session
        if request.session_id:
            session = db.query(ChatSession).filter(ChatSession.id == request.session_id).first()
            if not session:
                raise SessionNotFoundError(request.session_id)
        else:
            session = ChatSession(title=request.query[:50])  # Use first 50 chars as title
            db.add(session)
            db.commit()
            db.refresh(session)
            logger.info(f"Created new session: {session.id}")
        
        # Save user message
        user_message = Message(
            session_id=session.id,
            role="user",
            content=request.query
        )
        db.add(user_message)
        db.commit()
        db.refresh(user_message)
        
        # Get response from Gemini
        try:
            response_text = gemini_client.chat_with_files(request.query, request.file_uris)
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise GeminiAPIError(str(e))
        
        # Save assistant message
        assistant_message = Message(
            session_id=session.id,
            role="assistant",
            content=response_text
        )
        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)
        
        logger.info(f"Chat response generated for session: {session.id}")
        
        return ChatResponse(
            session_id=session.id,
            message=MessageResponse(
                id=user_message.id,
                role=user_message.role,
                content=user_message.content,
                created_at=user_message.created_at
            ),
            response=response_text
        )
    except (SessionNotFoundError, GeminiAPIError):
        raise
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents", response_model=DocumentListResponse)
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """List all uploaded documents with pagination."""
    try:
        logger.info(f"Listing documents (skip={skip}, limit={limit}, active_only={active_only})")
        
        query = db.query(Document)
        if active_only:
            query = query.filter(Document.is_active == True)
        
        total = query.count()
        documents = query.order_by(Document.uploaded_at.desc()).offset(skip).limit(limit).all()
        
        return DocumentListResponse(
            documents=[DocumentResponse.from_orm(doc) for doc in documents],
            total=total
        )
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/documents/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Delete a document (soft delete - marks as inactive)."""
    try:
        logger.info(f"Deleting document: {document_id}")
        
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise DocumentNotFoundError(document_id)
        
        # Soft delete
        document.is_active = False
        db.commit()
        
        # Optionally delete from Gemini
        try:
            gemini_client.delete_file(document.gemini_name)
            logger.info(f"Deleted file from Gemini: {document.gemini_name}")
        except Exception as e:
            logger.warning(f"Could not delete file from Gemini: {str(e)}")
        
        return {"message": f"Document {document_id} deleted successfully"}
    except DocumentNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sessions", response_model=ChatSessionResponse)
async def create_session(session: ChatSessionCreate, db: Session = Depends(get_db)):
    """Create a new chat session."""
    try:
        logger.info(f"Creating new session with title: {session.title}")
        
        db_session = ChatSession(title=session.title)
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        
        return ChatSessionResponse.from_orm(db_session)
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}/messages", response_model=SessionMessagesResponse)
async def get_session_messages(session_id: int, db: Session = Depends(get_db)):
    """Get all messages for a specific session."""
    try:
        logger.info(f"Getting messages for session: {session_id}")
        
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not session:
            raise SessionNotFoundError(session_id)
        
        messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at).all()
        
        return SessionMessagesResponse(
            session_id=session_id,
            messages=[MessageResponse.from_orm(msg) for msg in messages],
            total=len(messages)
        )
    except SessionNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error getting session messages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions", response_model=List[ChatSessionResponse])
async def list_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all chat sessions."""
    try:
        logger.info(f"Listing sessions (skip={skip}, limit={limit})")
        
        sessions = db.query(ChatSession).order_by(ChatSession.updated_at.desc()).offset(skip).limit(limit).all()
        
        return [ChatSessionResponse.from_orm(session) for session in sessions]
    except Exception as e:
        logger.error(f"Error listing sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
