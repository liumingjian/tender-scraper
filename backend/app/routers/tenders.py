"""API router for tender-related endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.tender import Tender
from app.schemas.tender import TenderResponse, TenderUpdate

router = APIRouter(prefix="/tenders", tags=["tenders"])


@router.get("", response_model=List[TenderResponse])
async def get_tenders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    source_name: Optional[str] = None,
    keyword: Optional[str] = None,
    min_budget: Optional[float] = None,
    max_budget: Optional[float] = None,
    include_filtered: bool = False,
    db: AsyncSession = Depends(get_db),
) -> List[TenderResponse]:
    """
    Get list of tender announcements with filtering.

    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        source_name: Filter by source name
        keyword: Search keyword in title and content
        min_budget: Minimum budget amount
        max_budget: Maximum budget amount
        include_filtered: Include filtered items (default: False)
        db: Database session

    Returns:
        List of tender announcements
    """
    # Build query
    query = select(Tender)

    # Apply filters
    conditions = []

    if not include_filtered:
        conditions.append(Tender.is_filtered == False)

    if source_name:
        conditions.append(Tender.source_name == source_name)

    if keyword:
        keyword_filter = f"%{keyword}%"
        conditions.append(
            (Tender.title.ilike(keyword_filter)) | (Tender.content.ilike(keyword_filter))
        )

    if min_budget is not None:
        conditions.append(Tender.budget_amount >= min_budget)

    if max_budget is not None:
        conditions.append(Tender.budget_amount <= max_budget)

    if conditions:
        query = query.where(and_(*conditions))

    # Apply ordering and pagination
    query = query.order_by(desc(Tender.created_at)).offset(skip).limit(limit)

    # Execute query
    result = await db.execute(query)
    tenders = result.scalars().all()

    return tenders


@router.get("/{tender_id}", response_model=TenderResponse)
async def get_tender(
    tender_id: int,
    db: AsyncSession = Depends(get_db),
) -> TenderResponse:
    """
    Get a specific tender by ID.

    Args:
        tender_id: Tender ID
        db: Database session

    Returns:
        Tender details
    """
    result = await db.execute(select(Tender).where(Tender.id == tender_id))
    tender = result.scalar_one_or_none()

    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")

    return tender


@router.patch("/{tender_id}", response_model=TenderResponse)
async def update_tender(
    tender_id: int,
    tender_update: TenderUpdate,
    db: AsyncSession = Depends(get_db),
) -> TenderResponse:
    """
    Update tender information (manual correction).

    Args:
        tender_id: Tender ID
        tender_update: Updated fields
        db: Database session

    Returns:
        Updated tender
    """
    result = await db.execute(select(Tender).where(Tender.id == tender_id))
    tender = result.scalar_one_or_none()

    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")

    # Update fields
    update_data = tender_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tender, field, value)

    await db.commit()
    await db.refresh(tender)

    return tender
