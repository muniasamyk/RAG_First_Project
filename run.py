"""
Application entry point.
Use this script to run the application in development mode.
"""
import uvicorn
from app.core.config import settings


def main():
    """Run the application with uvicorn."""
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info"
    )


if __name__ == "__main__":
    main()
