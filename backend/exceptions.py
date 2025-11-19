from fastapi import HTTPException, status


class DocumentUploadError(HTTPException):
    """Exception raised when document upload fails."""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Document upload failed: {detail}"
        )


class GeminiAPIError(HTTPException):
    """Exception raised when Gemini API call fails."""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gemini API error: {detail}"
        )


class SessionNotFoundError(HTTPException):
    """Exception raised when chat session is not found."""
    def __init__(self, session_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat session with id {session_id} not found"
        )


class DocumentNotFoundError(HTTPException):
    """Exception raised when document is not found."""
    def __init__(self, document_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id {document_id} not found"
        )


class FileSizeExceededError(HTTPException):
    """Exception raised when uploaded file size exceeds limit."""
    def __init__(self, max_size: int):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {max_size} bytes"
        )


class InvalidFileTypeError(HTTPException):
    """Exception raised when uploaded file type is not allowed."""
    def __init__(self, file_type: str, allowed_types: list):
        super().__init__(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type '{file_type}' is not allowed. Allowed types: {', '.join(allowed_types)}"
        )
