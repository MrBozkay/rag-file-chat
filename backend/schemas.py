from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Chat Session Schemas
class ChatSessionCreate(BaseModel):
    """Schema for creating a new chat session."""
    title: Optional[str] = Field(None, max_length=255, description="Optional title for the session")


class ChatSessionResponse(BaseModel):
    """Schema for chat session response."""
    id: int
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Document Schemas
class DocumentUploadResponse(BaseModel):
    """Schema for document upload response."""
    id: int
    filename: str
    original_filename: str
    mime_type: str
    file_size: int
    gemini_uri: str
    gemini_name: str
    uploaded_at: datetime


class DocumentResponse(BaseModel):
    """Schema for document response."""
    id: int
    filename: str
    original_filename: str
    mime_type: str
    file_size: int
    gemini_uri: str
    uploaded_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """Schema for document list response."""
    documents: List[DocumentResponse]
    total: int


# Message Schemas
class MessageResponse(BaseModel):
    """Schema for message response."""
    id: int
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    """Schema for chat request."""
    query: str = Field(..., min_length=1, max_length=5000, description="User query")
    session_id: Optional[int] = Field(None, description="Chat session ID. If not provided, a new session will be created")
    file_uris: List[str] = Field(default_factory=list, description="List of Gemini file URIs to use as context")


class ChatResponse(BaseModel):
    """Schema for chat response."""
    session_id: int
    message: MessageResponse
    response: str


class SessionMessagesResponse(BaseModel):
    """Schema for session messages response."""
    session_id: int
    messages: List[MessageResponse]
    total: int
