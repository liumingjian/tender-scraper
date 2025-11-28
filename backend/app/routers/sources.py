"""API router for source configuration."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.tender import SourceConfig
from app.schemas.tender import SourceConfigCreate, SourceConfigUpdate, SourceConfigResponse

router = APIRouter(prefix="/sources", tags=["sources"])


@router.post("", response_model=SourceConfigResponse, status_code=201)
async def create_source(
    source: SourceConfigCreate,
    db: AsyncSession = Depends(get_db),
) -> SourceConfigResponse:
    """Create a new data source configuration."""
    # Check if source with same name exists
    result = await db.execute(
        select(SourceConfig).where(SourceConfig.name == source.name)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Source with this name already exists")

    db_source = SourceConfig(**source.model_dump())
    db.add(db_source)
    await db.commit()
    await db.refresh(db_source)

    return db_source


@router.get("", response_model=List[SourceConfigResponse])
async def get_sources(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> List[SourceConfigResponse]:
    """Get list of data source configurations."""
    result = await db.execute(
        select(SourceConfig).offset(skip).limit(limit)
    )
    sources = result.scalars().all()
    return sources


@router.get("/{source_id}", response_model=SourceConfigResponse)
async def get_source(
    source_id: int,
    db: AsyncSession = Depends(get_db),
) -> SourceConfigResponse:
    """Get a specific source configuration."""
    result = await db.execute(
        select(SourceConfig).where(SourceConfig.id == source_id)
    )
    source = result.scalar_one_or_none()

    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    return source


@router.patch("/{source_id}", response_model=SourceConfigResponse)
async def update_source(
    source_id: int,
    source_update: SourceConfigUpdate,
    db: AsyncSession = Depends(get_db),
) -> SourceConfigResponse:
    """Update a source configuration."""
    result = await db.execute(
        select(SourceConfig).where(SourceConfig.id == source_id)
    )
    source = result.scalar_one_or_none()

    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    update_data = source_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(source, field, value)

    await db.commit()
    await db.refresh(source)

    return source


@router.delete("/{source_id}", status_code=204)
async def delete_source(
    source_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a source configuration."""
    result = await db.execute(
        select(SourceConfig).where(SourceConfig.id == source_id)
    )
    source = result.scalar_one_or_none()

    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    await db.delete(source)
    await db.commit()
