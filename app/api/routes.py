"""
API Routes for the Human Nutrition AI application.
"""
import time
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.models.schemas import QueryRequest, QueryResponse, HealthResponse
from app.services.rag_service import get_rag_service
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", include_in_schema=False)
async def serve_frontend():
    """Serve the main frontend HTML page."""
    return FileResponse(f"{settings.STATIC_DIR}/index.html")


@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    Returns service status and version information.
    """
    return HealthResponse(
        status="healthy",
        service=settings.APP_NAME,
        version=settings.APP_VERSION
    )


@router.post(
    "/api/rag", 
    response_model=QueryResponse, 
    tags=["RAG"],
    summary="Ask a nutrition question",
    description="Submit a nutrition-related question and receive an AI-generated answer."
)
async def ask_question(data: QueryRequest):
    """
    RAG Question-Answering endpoint.
    
    - **query**: A nutrition-related question (1-1000 characters)
    
    Returns an AI-generated answer based on the Human Nutrition document.
    """
    try:
        start_time = time.time()
        
        # Get RAG service and process query
        rag_service = get_rag_service()
        answer = rag_service.ask(data.query)
        
        response_time = (time.time() - start_time) * 1000
        logger.info(f"Query processed in {response_time:.2f}ms")
        
        return QueryResponse(
            answer=answer,
            response_time_ms=round(response_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your question. Please try again."
        )
