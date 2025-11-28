"""Simple HTTP-based scraper implementation."""
import logging
from typing import List, Dict, Any, Optional
import httpx
from bs4 import BeautifulSoup
from app.services.scraper.base import BaseScraper, ScrapedItem, ScraperConnectionError, ScraperParseError
from app.config import settings

logger = logging.getLogger(__name__)


class SimpleHttpScraper(BaseScraper):
    """HTTP scraper using httpx + BeautifulSoup."""

    def __init__(self, source_name: str, base_url: str, config: Dict[str, Any]) -> None:
        """
        Initialize HTTP scraper.

        Expected config keys:
            - list_url: URL to scrape list of announcements
            - list_selector: CSS selector for list items
            - title_selector: CSS selector for title
            - url_selector: CSS selector for detail URL
            - content_selector: CSS selector for content
            - date_selector: Optional CSS selector for published date
        """
        super().__init__(source_name, base_url, config)
        self.client = httpx.AsyncClient(
            timeout=settings.scraper_timeout,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
        )

    async def scrape(self, limit: int = 10) -> List[ScrapedItem]:
        """Scrape tender announcements."""
        try:
            list_url = self.config.get("list_url", self.base_url)
            response = await self.client.get(list_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")
            items = []

            # Find list items
            list_selector = self.config["list_selector"]
            item_elements = soup.select(list_selector)[:limit]

            logger.info(f"Found {len(item_elements)} items from {self.source_name}")

            for element in item_elements:
                try:
                    item = await self._parse_list_item(element)
                    if item:
                        items.append(item)
                except Exception as e:
                    logger.warning(f"Failed to parse item: {e}")
                    continue

            return items

        except httpx.HTTPError as e:
            raise ScraperConnectionError(f"HTTP error: {e}") from e
        except Exception as e:
            raise ScraperParseError(f"Parse error: {e}") from e

    async def _parse_list_item(self, element: BeautifulSoup) -> Optional[ScrapedItem]:
        """Parse a single list item."""
        # Extract title
        title_selector = self.config["title_selector"]
        title_elem = element.select_one(title_selector)
        if not title_elem:
            return None
        title = title_elem.get_text(strip=True)

        # Extract URL
        url_selector = self.config["url_selector"]
        url_elem = element.select_one(url_selector)
        if not url_elem:
            return None

        href = url_elem.get("href")
        if not href:
            return None

        # Make absolute URL
        if href.startswith("http"):
            url = href
        elif href.startswith("/"):
            url = self.base_url.rstrip("/") + href
        else:
            url = self.base_url.rstrip("/") + "/" + href

        # Extract content from detail page
        content, raw_html = await self._fetch_detail(url)

        # Extract published date if configured
        published_at = None
        if "date_selector" in self.config:
            date_elem = element.select_one(self.config["date_selector"])
            if date_elem:
                date_str = date_elem.get_text(strip=True)
                published_at = self._parse_date(date_str)

        return ScrapedItem(
            title=title,
            content=content,
            url=url,
            published_at=published_at,
            raw_html=raw_html,
        )

    async def _fetch_detail(self, url: str) -> tuple[str, str]:
        """Fetch detail page content."""
        try:
            response = await self.client.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")

            # Extract content
            content_selector = self.config["content_selector"]
            content_elem = soup.select_one(content_selector)

            if content_elem:
                content = content_elem.get_text(separator="\n", strip=True)
                raw_html = str(content_elem)
            else:
                content = soup.get_text(separator="\n", strip=True)
                raw_html = response.text

            return content, raw_html

        except Exception as e:
            logger.warning(f"Failed to fetch detail from {url}: {e}")
            return "", ""

    def _parse_date(self, date_str: str) -> Optional[Any]:
        """Parse date string to datetime."""
        try:
            from dateutil import parser
            return parser.parse(date_str)
        except Exception:
            return None

    async def test_connection(self) -> bool:
        """Test connection to source."""
        try:
            list_url = self.config.get("list_url", self.base_url)
            response = await self.client.get(list_url)
            return response.status_code == 200
        except Exception:
            return False

    async def close(self) -> None:
        """Close HTTP client."""
        await self.client.aclose()
