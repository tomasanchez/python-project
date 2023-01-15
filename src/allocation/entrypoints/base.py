"""
Base endpoints. Including health check and readiness.
"""

from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get(
    "/",
    include_in_schema=False,
    status_code=301,
)
def root_redirect():
    """
    Redirects the root path to the docs.
    """
    return RedirectResponse(url="/docs", status_code=301)
