from fastapi import FastAPI

from database.collections import SecretsCollection
from routers.secrets import router as secrets_router


async def configure_project():
    """Runs coroutines for the project configuration."""
    await SecretsCollection().create_ttl_index_on()


def create_app():
    """Creates instance of FastAPI class"""
    app = FastAPI(
        title="One time Secret",
        version="0.1",
        description="Service provides an opportunity to store your "
                    "one time secrets.",
        openapi_tags=[
            {
                "name": "Secrets",
                "description": "Operations with storing and retrieving users' secrets."
            }
        ]
    )
    app.include_router(secrets_router)
    return app
