"""Application configuration - FastAPI."""
from pydantic import BaseSettings

from allocation.version import __version__


class Application(BaseSettings):
    """Define application configuration model.
    Constructor will attempt to determine the values of any fields not passed
    as keyword arguments by reading from the environment. Default values will
    still be used if the matching environment variable is not set.
    Environment variables:
        * FASTAPI_DEBUG
        * FASTAPI_PROJECT_NAME
        * FASTAPI_VERSION
        * FASTAPI_DOCS_URL
        * FASTAPI_USE_SQLITE
    Attributes:
        DEBUG (bool): FastAPI logging level. You should disable this for
            production.
        PROJECT_NAME (str): FastAPI project name.
        VERSION (str): Application version.
        DOCS_URL (str): Path where swagger ui will be served at.
        USE_SQLITE (bool): Whether to use SQLite DB.
    """

    DEBUG: bool = True
    PROJECT_NAME: str = "Allocation Service"
    PROJECT_DESCRIPTION: str = "This service is responsible for allocating line orders on batch operations."
    VERSION: str = __version__
    DOCS_URL: str = "/docs"
    USE_SQLITE: bool = True

    # All your additional application configuration should go either here or in
    # separate file in this submodule.

    class Config:
        """Config subclass needed to customize BaseSettings settings.
        Attributes:
            case_sensitive (bool): When case_sensitive is True, the environment
                variable names must match field names (optionally with a prefix)
            env_prefix (str): The prefix for environment variable.
        Resources:
            https://pydantic-docs.helpmanual.io/usage/settings/
        """

        case_sensitive = True
        env_prefix = "FASTAPI_"


settings = Application()
