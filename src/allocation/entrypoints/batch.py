"""Batches Entry Point.

This module contains the entry point for the Batch resource.
"""

from fastapi import APIRouter, Depends

from allocation.domain.schemas import BatchIn
from allocation.service_layer.allocation_service import AllocationService
from allocation.service_layer.dependencies import get_uow
from allocation.service_layer.unit_of_work import AbstractUnitOfWork

router = APIRouter(prefix="/v1", tags=["batch"])


@router.post(
    "/batches",
    status_code=201,
    summary="Create a new batch",
)
def add_batch(
    batch: BatchIn,
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    """
    Adds a new batch.
    """
    service = AllocationService(uow)

    service.add_batch(**batch.dict())
