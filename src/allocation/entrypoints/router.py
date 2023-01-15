"""Application configuration - root APIRouter.
Defines all FastAPI application endpoints.

Resources:
    1. https://fastapi.tiangolo.com/tutorial/bigger-applications
"""
from fastapi import APIRouter

from allocation.entrypoints import allocation, base, batch

root_api_router = APIRouter(prefix="/api")
base_router = APIRouter()

# Base Routers
base_router.include_router(base.router)

# API Routers
root_api_router.include_router(batch.router)
root_api_router.include_router(allocation.router)
