"""Task service for running scraping and extraction pipeline."""
import logging
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender import Tender, SourceConfig
from app.schemas.tender import TenderCreate
from app.services.scraper.base import BaseScraper
from app.services.scraper.http_scraper import SimpleHttpScraper
from app.services.scraper.adapters import create_ccgp_scraper
from app.services.ai.extraction import extraction_service
from app.services.filter import filter_service

logger = logging.getLogger(__name__)


class TaskService:
    """Service for executing scraping and extraction tasks."""

    @staticmethod
    def create_scraper(source_config: SourceConfig) -> BaseScraper:
        """Create scraper instance based on source config."""
        if source_config.scraper_type == "http":
            return SimpleHttpScraper(
                source_name=source_config.name,
                base_url=source_config.url,
                config=source_config.config,
            )
        else:
            raise ValueError(f"Unsupported scraper type: {source_config.scraper_type}")

    async def run_source_task(
        self,
        db: AsyncSession,
        source_id: int,
        limit: int = 10,
    ) -> dict:
        """
        Run scraping task for a specific source.

        Args:
            db: Database session
            source_id: Source configuration ID
            limit: Maximum items to scrape

        Returns:
            Task result summary
        """
        # Get source config
        result = await db.execute(
            select(SourceConfig).where(SourceConfig.id == source_id)
        )
        source = result.scalar_one_or_none()

        if not source:
            raise ValueError(f"Source config {source_id} not found")

        if not source.is_active:
            raise ValueError(f"Source {source.name} is not active")

        # Create scraper
        scraper = self.create_scraper(source)

        try:
            # Scrape items
            logger.info(f"Starting scraping task for {source.name}")
            scraped_items = await scraper.scrape(limit=limit)
            logger.info(f"Scraped {len(scraped_items)} items from {source.name}")

            # Process each item
            processed = 0
            filtered = 0
            errors = 0

            for item in scraped_items:
                try:
                    # Check if already exists
                    existing = await db.execute(
                        select(Tender).where(
                            Tender.source_name == source.name,
                            Tender.source_url == item.url,
                        )
                    )
                    if existing.scalar_one_or_none():
                        logger.debug(f"Item already exists: {item.url}")
                        continue

                    # Apply keyword filters first
                    is_filtered, filter_reason = filter_service.apply_filters(
                        title=item.title,
                        content=item.content,
                        filter_rules=source.filter_rules,
                    )

                    # Extract structured data
                    extracted_data = None
                    if not is_filtered:
                        try:
                            extracted_data = await extraction_service.extract(
                                title=item.title,
                                content=item.content,
                            )
                        except Exception as e:
                            logger.warning(f"Extraction failed for {item.title}: {e}")

                    # Apply budget filters if extraction succeeded
                    if extracted_data and not is_filtered:
                        is_budget_filtered, budget_reason = filter_service.apply_budget_filters(
                            budget_amount=extracted_data.budget_amount,
                            filter_rules=source.filter_rules,
                        )
                        if is_budget_filtered:
                            is_filtered = True
                            filter_reason = budget_reason

                    # Create tender record
                    tender = Tender(
                        source_name=source.name,
                        source_url=item.url,
                        original_id=item.original_id,
                        title=item.title,
                        content=item.content,
                        raw_html=item.raw_html,
                        published_at=item.published_at,
                        is_filtered=is_filtered,
                        filter_reason=filter_reason,
                    )

                    # Add extracted fields
                    if extracted_data:
                        tender.project_name = extracted_data.project_name
                        tender.budget_amount = extracted_data.budget_amount
                        tender.budget_currency = extracted_data.budget_currency
                        tender.deadline = extracted_data.deadline
                        tender.contact_person = extracted_data.contact_person
                        tender.contact_phone = extracted_data.contact_phone
                        tender.contact_email = extracted_data.contact_email
                        tender.location = extracted_data.location
                        tender.extracted_data = extracted_data.model_dump()

                    db.add(tender)
                    await db.flush()

                    if is_filtered:
                        filtered += 1
                    else:
                        processed += 1

                except Exception as e:
                    logger.error(f"Error processing item {item.url}: {e}")
                    errors += 1
                    continue

            # Commit all changes
            await db.commit()

            # Update source last run time
            from datetime import datetime
            source.last_run_at = datetime.now()
            await db.commit()

            logger.info(
                f"Task completed for {source.name}: "
                f"processed={processed}, filtered={filtered}, errors={errors}"
            )

            return {
                "source_name": source.name,
                "scraped": len(scraped_items),
                "processed": processed,
                "filtered": filtered,
                "errors": errors,
            }

        finally:
            await scraper.close()

    async def run_all_active_sources(
        self,
        db: AsyncSession,
        limit: int = 10,
    ) -> List[dict]:
        """Run tasks for all active sources."""
        # Get all active sources
        result = await db.execute(
            select(SourceConfig).where(SourceConfig.is_active == True)
        )
        sources = result.scalars().all()

        results = []
        for source in sources:
            try:
                result = await self.run_source_task(db, source.id, limit)
                results.append(result)
            except Exception as e:
                logger.error(f"Task failed for {source.name}: {e}")
                results.append({
                    "source_name": source.name,
                    "error": str(e),
                })

        return results


# Create singleton instance
task_service = TaskService()
