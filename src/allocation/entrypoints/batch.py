"""Batches Entry Point.

This module contains the entry point for the Batch resource.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from allocation.adapters.repository import AbstractRepository
from allocation.domain.schemas import BatchIn
from allocation.service_layer.allocation_service import AllocationService
from allocation.service_layer.dependencies import get_batch_repository, get_session

router = APIRouter(prefix="/v1", tags=["batch"])


@router.post(
    "/batches",
    status_code=201,
    summary="Create a new batch",
)
def add_batch(
    batch: BatchIn,
    session: Session = Depends(get_session),
    batch_repository: AbstractRepository = Depends(get_batch_repository),
):
    """
    Adds a new batch.
    """
    service = AllocationService(batch_repository, session)

    service.add_batch(**batch.dict())
