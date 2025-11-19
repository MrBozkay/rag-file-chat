from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # API Keys
    google_api_key: str
    
    # Database
    database_url: str = "sqlite:///./rag_chat.db"
    
    # File Upload Settings
    max_file_size: int = 10485760  # 10MB in bytes
    allowed_file_types: str = "application/pdf,text/plain,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def allowed_file_types_list(self) -> List[str]:
        """Convert comma-separated string to list."""
        return [ft.strip() for ft in self.allowed_file_types.split(",")]
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated string to list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
