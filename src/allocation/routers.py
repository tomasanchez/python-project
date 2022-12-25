"""
This module describes the allocation service available endpoints.
"""
import logging
from logging.config import dictConfig

from fastapi import APIRouter, Depends, HTTPException

from allocation.dependencies import get_batch_repository
from allocation.domain import models, schemas
from allocation.repository import repository
from allocation.settings.config import LogConfig

router = APIRouter(prefix="/v1", tags=["allocation"])

dictConfig(LogConfig().dict())
logger = logging.getLogger("allocation_service")


@router.post("/allocate", status_code=201)
def allocate(order: schemas.OrderLine, batch_repository: repository.AbstractRepository = Depends(get_batch_repository)):
    """
    Allocates an order line.
    """
    logger.info("Allocating order (%s)", order)
    line = models.OrderLine(order.order_id, order.sku, order.qty)
    batches: list[models.Batch] = batch_repository.find_all()

    for batch in batches:
        if batch.can_allocate(line):
            batch.allocate(line)
            batch_repository.save(batch)
            logger.info("Allocated batch (%s)", batch)
            return {"reference": batch.reference}

    logger.error("Could not allocate for order (%s)", order)
    raise HTTPException(status_code=404, detail="Could not allocate. No batches found")
