"""Base scraper abstract class."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScrapedItem:
    """Data class for scraped tender announcement."""

    title: str
    content: str
    url: str
    original_id: Optional[str] = None
    published_at: Optional[datetime] = None
    raw_html: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self) -> None:
        """Initialize metadata if not provided."""
        if self.metadata is None:
            self.metadata = {}


class BaseScraper(ABC):
    """Abstract base class for all scrapers."""

    def __init__(self, source_name: str, base_url: str, config: Dict[str, Any]) -> None:
        """
        Initialize scraper.

        Args:
            source_name: Name of the data source
            base_url: Base URL of the target website
            config: Configuration dictionary for the scraper
        """
        self.source_name = source_name
        self.base_url = base_url
        self.config = config

    @abstractmethod
    async def scrape(self, limit: int = 10) -> List[ScrapedItem]:
        """
        Scrape tender announcements from the source.

        Args:
            limit: Maximum number of items to scrape

        Returns:
            List of scraped items

        Raises:
            ScraperException: If scraping fails
        """
        pass

    @abstractmethod
    async def test_connection(self) -> bool:
        """
        Test if the scraper can connect to the source.

        Returns:
            True if connection successful, False otherwise
        """
        pass

    async def close(self) -> None:
        """Clean up resources (override if needed)."""
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(source='{self.source_name}')>"


class ScraperException(Exception):
    """Base exception for scraper errors."""

    pass


class ScraperConnectionError(ScraperException):
    """Raised when scraper cannot connect to source."""

    pass


class ScraperParseError(ScraperException):
    """Raised when scraper cannot parse content."""

    pass
