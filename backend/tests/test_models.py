"""Tests for database models."""
import pytest
from datetime import datetime
from sqlalchemy import select

from app.models.tender import Tender, SourceConfig


@pytest.mark.asyncio
async def test_create_tender(test_db):
    """Test creating a tender record."""
    tender = Tender(
        source_name="测试数据源",
        source_url="https://example.com/tender/1",
        title="测试招标项目",
        content="这是测试内容",
        budget_amount=500000,
        is_filtered=False,
    )

    test_db.add(tender)
    await test_db.commit()
    await test_db.refresh(tender)

    assert tender.id is not None
    assert tender.source_name == "测试数据源"
    assert tender.budget_amount == 500000
    assert tender.created_at is not None


@pytest.mark.asyncio
async def test_create_source_config(test_db):
    """Test creating a source config."""
    source = SourceConfig(
        name="测试网站",
        url="https://example.com",
        scraper_type="http",
        config={"list_selector": "ul.items > li"},
        is_active=True,
    )

    test_db.add(source)
    await test_db.commit()
    await test_db.refresh(source)

    assert source.id is not None
    assert source.name == "测试网站"
    assert source.scraper_type == "http"
    assert source.is_active is True


@pytest.mark.asyncio
async def test_query_tenders(test_db):
    """Test querying tenders."""
    # Create test data
    tender1 = Tender(
        source_name="源1",
        source_url="https://example.com/1",
        title="项目1",
        content="内容1",
        budget_amount=100000,
        is_filtered=False,
    )
    tender2 = Tender(
        source_name="源2",
        source_url="https://example.com/2",
        title="项目2",
        content="内容2",
        budget_amount=500000,
        is_filtered=True,
    )

    test_db.add_all([tender1, tender2])
    await test_db.commit()

    # Query all
    result = await test_db.execute(select(Tender))
    tenders = result.scalars().all()
    assert len(tenders) == 2

    # Query non-filtered
    result = await test_db.execute(
        select(Tender).where(Tender.is_filtered == False)
    )
    tenders = result.scalars().all()
    assert len(tenders) == 1
    assert tenders[0].title == "项目1"
