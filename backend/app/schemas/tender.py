"""Pydantic schemas for tender data validation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class TenderExtractModel(BaseModel):
    """Model for AI-extracted tender information."""

    project_name: Optional[str] = Field(None, description="Project name")
    budget_amount: Optional[float] = Field(None, ge=0, description="Budget amount")
    budget_currency: Optional[str] = Field("CNY", description="Currency code")
    deadline: Optional[datetime] = Field(None, description="Submission deadline")
    contact_person: Optional[str] = Field(None, max_length=100)
    contact_phone: Optional[str] = Field(None, max_length=50)
    contact_email: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=200)

    @field_validator("budget_amount", mode="before")
    @classmethod
    def parse_budget(cls, v: any) -> Optional[float]:
        """Parse budget from various formats."""
        if v is None or v == "":
            return None
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            # Remove common Chinese characters and convert
            cleaned = v.replace("元", "").replace("万", "0000").replace(",", "").strip()
            try:
                return float(cleaned)
            except ValueError:
                return None
        return None

    @field_validator("deadline", mode="before")
    @classmethod
    def parse_deadline(cls, v: any) -> Optional[datetime]:
        """Parse deadline from string."""
        if v is None or v == "":
            return None
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            from dateutil import parser
            try:
                return parser.parse(v)
            except Exception:
                return None
        return None


class TenderCreate(BaseModel):
    """Schema for creating a tender."""

    source_name: str
    source_url: str
    original_id: Optional[str] = None
    title: str
    content: str
    raw_html: Optional[str] = None
    published_at: Optional[datetime] = None


class TenderUpdate(BaseModel):
    """Schema for updating a tender."""

    project_name: Optional[str] = None
    budget_amount: Optional[float] = None
    budget_currency: Optional[str] = None
    deadline: Optional[datetime] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    location: Optional[str] = None
    is_manually_corrected: bool = True


class TenderResponse(BaseModel):
    """Schema for tender API response."""

    id: int
    source_name: str
    source_url: str
    title: str
    content: str
    project_name: Optional[str] = None
    budget_amount: Optional[float] = None
    budget_currency: Optional[str] = None
    deadline: Optional[datetime] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    location: Optional[str] = None
    is_filtered: bool
    filter_reason: Optional[str] = None
    is_manually_corrected: bool
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SourceConfigCreate(BaseModel):
    """Schema for creating a source config."""

    name: str
    url: str
    scraper_type: str = Field(..., pattern="^(http|browser)$")
    config: dict = Field(default_factory=dict)
    filter_rules: Optional[dict] = None
    is_active: bool = True
    schedule_cron: Optional[str] = None


class SourceConfigUpdate(BaseModel):
    """Schema for updating a source config."""

    url: Optional[str] = None
    config: Optional[dict] = None
    filter_rules: Optional[dict] = None
    is_active: Optional[bool] = None
    schedule_cron: Optional[str] = None


class SourceConfigResponse(BaseModel):
    """Schema for source config API response."""

    id: int
    name: str
    url: str
    scraper_type: str
    config: dict
    filter_rules: Optional[dict] = None
    is_active: bool
    schedule_cron: Optional[str] = None
    last_run_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
