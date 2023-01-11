"""
This module contains the main entry point for the allocation service.
"""

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from allocation.routers import router

app = FastAPI(
    title="Allocation Service",
    description="This service is responsible for allocating line orders on batch operations.",
)

app.include_router(prefix="/api", router=router)


@app.get("/", include_in_schema=False, status_code=301)
def root_redirect():
    """
    Redirects the root path to the docs.
    """
    return RedirectResponse(url="/docs", status_code=301)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app")
