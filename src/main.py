"""
FastAPI Challenge - Main Application
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.services.logging import logger
from src.api.routes.game import router as game_router
from src.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting FastAPI Challenge Application...")
    logger.info(f"🌐 Environment: {settings.ENVIRONMENT}")
    logger.debug(f"📝 Debug mode: {settings.DEBUG}")

    yield

    # Shutdown
    logger.warning("👋 Shutting down FastAPI Challenge Application...")


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="A FastAPI challenge project with Docker support",
        version=settings.VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(game_router, prefix="/api/v1")

    # Root endpoint
    @app.get("/")
    async def root():
        """
        Root endpoint with API information
        """
        return JSONResponse(
            content={
                "message": "Welcome to FastAPI Challenge!",
                "version": settings.VERSION,
                "environment": settings.ENVIRONMENT,
                "docs": (
                    "/docs"
                    if settings.DEBUG
                    else "Documentation disabled in production"
                ),
            }
        )

    @app.get("/health", tags=["health"])
    async def health_check():
        """
        Health check endpoint
        """
        return JSONResponse(content={"status": "ok"})

    return app


# Create the application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.WORKERS,
    )
