"""Example script for running a scraping task."""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.database import AsyncSessionLocal
from app.models.tender import SourceConfig
from app.services.scraper.adapters import create_ccgp_scraper
from app.services.ai.extraction import extraction_service


async def main():
    """Run example scraping task."""
    print("Creating scraper for China Government Procurement website...")

    # Create scraper
    scraper = create_ccgp_scraper()

    try:
        # Test connection
        print("Testing connection...")
        is_connected = await scraper.test_connection()
        print(f"Connection status: {is_connected}")

        if not is_connected:
            print("Failed to connect to source")
            return

        # Scrape items
        print("\nScraping items (limit: 3)...")
        items = await scraper.scrape(limit=3)
        print(f"Scraped {len(items)} items")

        # Process each item
        for i, item in enumerate(items, 1):
            print(f"\n--- Item {i} ---")
            print(f"Title: {item.title[:80]}...")
            print(f"URL: {item.url}")
            print(f"Content length: {len(item.content)} chars")

            # Extract structured data
            if os.getenv("GEMINI_API_KEY"):
                print("Extracting structured data...")
                extracted = await extraction_service.extract(
                    title=item.title,
                    content=item.content,
                )

                if extracted:
                    print(f"Project: {extracted.project_name}")
                    print(f"Budget: {extracted.budget_amount} {extracted.budget_currency}")
                    print(f"Deadline: {extracted.deadline}")
                    print(f"Contact: {extracted.contact_person} ({extracted.contact_phone})")
                else:
                    print("Extraction failed")
            else:
                print("Skipping extraction (no API key)")

    finally:
        await scraper.close()


if __name__ == "__main__":
    asyncio.run(main())
