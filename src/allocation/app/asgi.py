"""Application implementation - ASGI."""
import logging

from fastapi import FastAPI

from allocation.adapters import database
from allocation.adapters.orm import metadata
from allocation.app.config.settings import settings
from allocation.app.router import base_router, root_api_router
from allocation.app.utils.aiohttp_client import AiohttpClient

log = logging.getLogger(__name__)


async def on_startup():
    """Define FastAPI startup event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#startup-event
    """
    log.debug("Execute FastAPI startup event handler.")

    if settings.USE_SQLITE:
        metadata.create_all(database.engine)

    AiohttpClient.get_aiohttp_client()


async def on_shutdown():
    """Define FastAPI shutdown event handler.
    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#shutdown-event
    """
    log.debug("Execute FastAPI shutdown event handler.")

    await AiohttpClient.close_aiohttp_client()


def get_application() -> FastAPI:
    """Initialize FastAPI application.
    Returns:
       FastAPI: Application object instance.
    """
    log.debug("Initialize FastAPI application node.")

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        debug=settings.DEBUG,
        version=settings.VERSION,
        docs_url=settings.DOCS_URL,
        on_startup=[on_startup],
        on_shutdown=[on_shutdown],
    )

    log.debug("Add application routes.")

    app.include_router(base_router)
    app.include_router(root_api_router)

    return app
