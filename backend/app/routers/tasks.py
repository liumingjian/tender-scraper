"""API router for task execution."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.task import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


class RunTaskRequest(BaseModel):
    """Request model for running a task."""

    source_id: Optional[int] = None
    limit: int = 10


class RunTaskResponse(BaseModel):
    """Response model for task execution."""

    success: bool
    message: str
    results: list


@router.post("/run", response_model=RunTaskResponse)
async def run_task(
    request: RunTaskRequest,
    db: AsyncSession = Depends(get_db),
) -> RunTaskResponse:
    """
    Run scraping and extraction task.

    Args:
        request: Task configuration
        db: Database session

    Returns:
        Task execution results
    """
    try:
        if request.source_id:
            # Run task for specific source
            result = await task_service.run_source_task(
                db=db,
                source_id=request.source_id,
                limit=request.limit,
            )
            results = [result]
            message = f"Task completed for source {request.source_id}"
        else:
            # Run tasks for all active sources
            results = await task_service.run_all_active_sources(
                db=db,
                limit=request.limit,
            )
            message = f"Tasks completed for {len(results)} sources"

        return RunTaskResponse(
            success=True,
            message=message,
            results=results,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task execution failed: {e}")
