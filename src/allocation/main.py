"""
This module contains the main entry point for the allocation service.
"""

from fastapi import FastAPI

from allocation.entrypoints.router import base_router, root_api_router

app = FastAPI(
    title="Allocation Service",
    description="This service is responsible for allocating line orders on batch operations.",
)

app.include_router(base_router)
app.include_router(root_api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app")
