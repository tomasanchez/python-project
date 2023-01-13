"""
This module describes the allocation service available endpoints.
"""
import logging
from logging.config import dictConfig

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from allocation.adapters import repository
from allocation.domain import schemas
from allocation.service_layer.allocation_service import AllocationService, InvalidSku, NoBatchesAvailable, OutOfStock
from allocation.service_layer.dependencies import get_batch_repository, get_session
from allocation.settings.config import LogConfig

router = APIRouter(prefix="/v1", tags=["allocation"])

dictConfig(LogConfig().dict())
logger = logging.getLogger("allocation_service")


@router.post("/allocations", status_code=201)
def allocate(
    order: schemas.OrderLine,
    batch_repository: repository.AbstractRepository = Depends(get_batch_repository),
    session: Session = Depends(get_session),
):
    """
    Allocates an order line.
    """
    logger.info("Allocating order (%s)", order)

    try:
        service = AllocationService(batch_repository, session)
        batch_ref = service.allocate(**order.dict())
    except (InvalidSku, OutOfStock) as e:
        logger.error("Could not allocate for order (%s)", order)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except NoBatchesAvailable as e:
        logger.warning("No batches available")
        raise HTTPException(status_code=404, detail=str(e)) from e

    return {"reference": batch_ref}
