import logging
import sys
from pathlib import Path
from datetime import datetime
from config import settings

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Create logger
logger = logging.getLogger("rag_chat")
logger.setLevel(getattr(logging, settings.log_level.upper()))

# Create formatters
detailed_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

simple_formatter = logging.Formatter(
    '%(levelname)s - %(message)s'
)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(simple_formatter)

# File handler
log_file = logs_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(detailed_formatter)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def get_logger(name: str = None) -> logging.Logger:
    """Get a logger instance."""
    if name:
        return logging.getLogger(f"rag_chat.{name}")
    return logger
