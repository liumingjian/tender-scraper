"""Database models for tenders and source configurations."""
from datetime import datetime
from typing import Optional
from sqlalchemy import JSON, String, Text, DateTime, Numeric, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class Tender(Base):
    """Tender announcement model."""

    __tablename__ = "tenders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Source information
    source_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    original_id: Mapped[Optional[str]] = mapped_column(String(200), index=True)

    # Core fields
    title: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Extracted fields
    project_name: Mapped[Optional[str]] = mapped_column(Text)
    budget_amount: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    budget_currency: Mapped[Optional[str]] = mapped_column(String(10))
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    contact_person: Mapped[Optional[str]] = mapped_column(String(100))
    contact_phone: Mapped[Optional[str]] = mapped_column(String(50))
    contact_email: Mapped[Optional[str]] = mapped_column(String(100))
    location: Mapped[Optional[str]] = mapped_column(String(200))

    # Metadata
    raw_html: Mapped[Optional[str]] = mapped_column(Text)
    extracted_data: Mapped[Optional[dict]] = mapped_column(JSON)

    # Status
    is_filtered: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    filter_reason: Mapped[Optional[str]] = mapped_column(Text)
    is_manually_corrected: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Tender(id={self.id}, title='{self.title[:50]}...')>"


class SourceConfig(Base):
    """Data source configuration model."""

    __tablename__ = "source_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Basic info
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    scraper_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'http' or 'browser'

    # Scraper config
    config: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    # Filter rules
    filter_rules: Mapped[Optional[dict]] = mapped_column(JSON)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

    # Schedule
    schedule_cron: Mapped[Optional[str]] = mapped_column(String(100))

    # Timestamps
    last_run_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<SourceConfig(id={self.id}, name='{self.name}')>"
