"""
FastAPI Application Factory.
Creates and configures the FastAPI application instance.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import router
from app.services.rag_service import get_rag_service

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Pre-warms the RAG model on startup for faster first response.
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Pre-warm the RAG service
    try:
        get_rag_service()
        logger.info("RAG service initialized and ready!")
    except Exception as e:
        logger.error(f"Failed to initialize RAG service: {e}")
        raise
    
    yield
    
    logger.info(f"Shutting down {settings.APP_NAME}")


def create_app() -> FastAPI:
    """
    Application factory function.
    Creates and configures the FastAPI application.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="AI-powered nutrition assistant using RAG (Retrieval-Augmented Generation)",
        version=settings.APP_VERSION,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Configure CORS
    origins = settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS != "*" else ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Mount static files
    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
    
    # Include API routes
    app.include_router(router)
    
    return app


# Create app instance
app = create_app()
