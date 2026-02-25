"""
Pydantic models/schemas for request and response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional


class QueryRequest(BaseModel):
    """Request model for RAG queries."""
    query: str = Field(
        ..., 
        min_length=1, 
        max_length=1000,
        description="The nutrition-related question to ask",
        examples=["What are the main sources of Vitamin C?"]
    )


class QueryResponse(BaseModel):
    """Response model for RAG queries."""
    answer: str = Field(..., description="The AI-generated answer")
    response_time_ms: float = Field(..., description="Processing time in milliseconds")
    

class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")


class ErrorResponse(BaseModel):
    """Response model for errors."""
    detail: str = Field(..., description="Error message")
