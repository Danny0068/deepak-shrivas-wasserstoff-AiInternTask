from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import APIKeyHeader
import time
import logging
from typing import Callable
import os
from dotenv import load_dotenv
from datetime import datetime

from app.routes.query_router import router as query_router
from app.routes.document_router import router as document_router
from app.services.vector_store import get_chroma_collection

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# API key security
API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

# Create FastAPI app
app = FastAPI(
    title="Document Query API",
    description="API for querying and managing documents",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Error handling middleware
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next: Callable):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

# Include routers
app.include_router(
    query_router,
    prefix="/api",
    tags=["query"],
    responses={
        200: {"description": "Successful response"},
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"}
    }
)

app.include_router(
    document_router,
    prefix="/api",
    tags=["documents"],
    responses={
        200: {"description": "Successful response"},
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    }
)

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "message": "Welcome to Theme Identifier API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

@app.get("/api/health")
async def health_check(api_key: str = Depends(API_KEY_HEADER)):
    """Health check endpoint."""
    try:
        # Check if vector store is accessible
        from app.services.vector_store import get_chroma_collection
        collection = get_chroma_collection()
        
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "vector_store": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "degraded",
            "timestamp": time.time(),
            "error": str(e)
        }
