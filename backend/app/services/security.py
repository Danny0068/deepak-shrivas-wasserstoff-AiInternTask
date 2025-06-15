import os
import logging
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from typing import Optional

# Configure logging
logger = logging.getLogger(__name__)

# Get API key from environment variable
API_KEY = os.getenv("API_KEY", "development-key-123")

# Configure API key header
API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    """Verify the API key."""
    try:
        if api_key != API_KEY:
            logger.warning(f"Invalid API key attempt: {api_key}")
            raise HTTPException(
                status_code=401,
                detail="Invalid API key"
            )
        return api_key
    except Exception as e:
        logger.error(f"Error verifying API key: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        ) 