from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time

from api.routes import router
from database import init_db
from config import settings
from logger import get_logger
from exceptions import (
    DocumentUploadError, GeminiAPIError, SessionNotFoundError,
    DocumentNotFoundError, FileSizeExceededError, InvalidFileTypeError
)

logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown."""
    # Startup
    logger.info("Starting up application...")
    init_db()
    logger.info("Database initialized")
    yield
    # Shutdown
    logger.info("Shutting down application...")


app = FastAPI(
    title="RAG File Chat API",
    description="Backend API for RAG-based file chat application using Google Gemini",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    start_time = time.time()
    
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"Request completed: {request.method} {request.url.path} - "
        f"Status: {response.status_code} - Time: {process_time:.3f}s"
    )
    
    return response


# Global exception handlers
@app.exception_handler(DocumentUploadError)
async def document_upload_error_handler(request: Request, exc: DocumentUploadError):
    """Handle document upload errors."""
    logger.error(f"Document upload error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(GeminiAPIError)
async def gemini_api_error_handler(request: Request, exc: GeminiAPIError):
    """Handle Gemini API errors."""
    logger.error(f"Gemini API error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(SessionNotFoundError)
async def session_not_found_error_handler(request: Request, exc: SessionNotFoundError):
    """Handle session not found errors."""
    logger.warning(f"Session not found: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(DocumentNotFoundError)
async def document_not_found_error_handler(request: Request, exc: DocumentNotFoundError):
    """Handle document not found errors."""
    logger.warning(f"Document not found: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(FileSizeExceededError)
async def file_size_exceeded_error_handler(request: Request, exc: FileSizeExceededError):
    """Handle file size exceeded errors."""
    logger.warning(f"File size exceeded: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(InvalidFileTypeError)
async def invalid_file_type_error_handler(request: Request, exc: InvalidFileTypeError):
    """Handle invalid file type errors."""
    logger.warning(f"Invalid file type: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred"}
    )


# Include routers
app.include_router(router, prefix="/api", tags=["API"])


@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "message": "Welcome to RAG File Chat API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
