"""Adapter for China Government Procurement website (ccgp.gov.cn)."""
from typing import Dict, Any
from app.services.scraper.http_scraper import SimpleHttpScraper


def create_ccgp_scraper() -> SimpleHttpScraper:
    """
    Create scraper for China Government Procurement website.

    Example URL: http://www.ccgp.gov.cn/cggg/dfgg/
    """
    config: Dict[str, Any] = {
        "list_url": "http://www.ccgp.gov.cn/cggg/dfgg/",
        "list_selector": "ul.vT-srch-result-list-bid > li",
        "title_selector": "a",
        "url_selector": "a",
        "content_selector": "div.vF_detail_content, div.article",
        "date_selector": "span.time",
    }

    return SimpleHttpScraper(
        source_name="中国政府采购网",
        base_url="http://www.ccgp.gov.cn",
        config=config,
    )


def create_custom_scraper(
    source_name: str,
    base_url: str,
    list_selector: str,
    title_selector: str,
    url_selector: str,
    content_selector: str,
    date_selector: str = None,
    list_url: str = None,
) -> SimpleHttpScraper:
    """
    Create a custom HTTP scraper with specified selectors.

    Args:
        source_name: Name of the data source
        base_url: Base URL of the website
        list_selector: CSS selector for list items
        title_selector: CSS selector for title within list item
        url_selector: CSS selector for URL within list item
        content_selector: CSS selector for content on detail page
        date_selector: Optional CSS selector for published date
        list_url: Optional list URL (defaults to base_url)

    Returns:
        Configured SimpleHttpScraper instance
    """
    config: Dict[str, Any] = {
        "list_url": list_url or base_url,
        "list_selector": list_selector,
        "title_selector": title_selector,
        "url_selector": url_selector,
        "content_selector": content_selector,
    }

    if date_selector:
        config["date_selector"] = date_selector

    return SimpleHttpScraper(
        source_name=source_name,
        base_url=base_url,
        config=config,
    )
