"""
This module describes the allocation service available endpoints.
"""
import logging
from logging.config import dictConfig

from fastapi import APIRouter, Depends, HTTPException

from allocation.adapters import repository
from allocation.domain import models, schemas
from allocation.entrypoints.dependencies import get_batch_repository
from allocation.service_layer.allocation_service import AllocationService, InvalidSku, NoBatchesAvailable, OutOfStock
from allocation.settings.config import LogConfig

router = APIRouter(prefix="/v1", tags=["allocation"])

dictConfig(LogConfig().dict())
logger = logging.getLogger("allocation_service")


@router.post("/allocate", status_code=201)
def allocate(
    order: schemas.OrderLine,
    batch_repository: repository.AbstractRepository = Depends(get_batch_repository),
):
    """
    Allocates an order line.
    """
    logger.info("Allocating order (%s)", order)
    line = models.OrderLine(order.order_id, order.sku, order.qty)

    try:
        service = AllocationService(batch_repository)
        batch_ref = service.allocate(line)
    except (InvalidSku, OutOfStock) as e:
        logger.error("Could not allocate for order (%s)", order)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except NoBatchesAvailable as e:
        logger.warning("No batches available")
        raise HTTPException(status_code=404, detail=str(e)) from e

    return {"reference": batch_ref}
