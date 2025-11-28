"""Application configuration settings."""
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/tender_scraper"

    # Gemini API
    gemini_api_key: str
    gemini_model: str = "gemini-2.0-flash-exp"
    gemini_temperature: float = 0.5

    # App
    debug: bool = False
    environment: str = "development"

    # API
    api_v1_prefix: str = "/api/v1"

    # Scraping
    scraper_timeout: int = 30
    scraper_max_retries: int = 3


settings = Settings()
