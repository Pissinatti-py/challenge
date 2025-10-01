from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """

    PROJECT_NAME: str = Field(default="FastAPI Challenge", description="Project name")

    VERSION: str = Field(default="0.1.0", description="Application version")

    DESCRIPTION: str = Field(
        default="A FastAPI challenge project with Docker support",
        description="Application description",
    )

    ENVIRONMENT: str = Field(default="development", description="Environment name")

    DEBUG: bool = Field(default=True, description="Debug mode")

    HOST: str = Field(default="0.0.0.0", description="Server host")

    PORT: int = Field(default=8000, description="Server port")

    WORKERS: int = Field(default=1, description="Number of workers")

    # ALLOWED_HOSTS: List[str] = Field(
    #     default=["*"],
    #     description="Allowed hosts for CORS"
    # )

    SECRET_KEY: str = Field(
        default="your-secret-key-here-change-in-production",
        description="Secret key for JWT tokens",
    )

    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")

    API_V1_STR: str = Field(default="/api/v1", description="API v1 prefix")

    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    RATE_LIMIT_PER_MINUTE: int = Field(default=60, description="Rate limit per minute")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Override settings based on environment
        if self.ENVIRONMENT.lower() == "production":
            self.DEBUG = False

        elif self.ENVIRONMENT.lower() == "testing":
            self.DEBUG = True


# Create global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get application settings instance
    """
    return settings
