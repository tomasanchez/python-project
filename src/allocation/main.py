"""
This module contains the main entry point for the allocation service.
"""
from allocation.app.asgi import get_application

app = get_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app")
