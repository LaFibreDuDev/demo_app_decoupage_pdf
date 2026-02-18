"""Centralised configuration — all values are read from the .env file.

Never hardcode configuration values directly in route or service modules.
Always import from this module instead.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the backend directory
_env_path = Path(__file__).parent / ".env"
load_dotenv(_env_path)

# Upload
UPLOAD_MAX_SIZE_MB: int = int(os.getenv("UPLOAD_MAX_SIZE_MB", "10"))
UPLOAD_MAX_SIZE_BYTES: int = UPLOAD_MAX_SIZE_MB * 1024 * 1024

# Storage
TEMP_DIR: str = os.getenv("TEMP_DIR", "/tmp/pdf_splitter")

# Session lifetime
SESSION_TTL_HOURS: int = int(os.getenv("SESSION_TTL_HOURS", "24"))

# Thumbnails
THUMB_DPI: int = int(os.getenv("THUMB_DPI", "150"))

# CORS — comma-separated list of allowed origins
ALLOWED_ORIGINS: list[str] = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
]

# Session key derivation secret — must be set in production (min 32 bytes)
_raw_secret = os.getenv("SESSION_SECRET", "")
if not _raw_secret:
    raise RuntimeError("SESSION_SECRET must be set in the environment.")
SESSION_SECRET: bytes = _raw_secret.encode()
