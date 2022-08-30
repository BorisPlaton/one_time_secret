#!/usr/bin/env python
import uvicorn
from fastapi import FastAPI

from config.settings import settings
from routers.secrets import router as secrets_router


def create_app():
    """Creates instance of FastAPI class"""
    app_ = FastAPI(
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
    app_.include_router(secrets_router)
    return app_


if __name__ == '__main__':
    uvicorn.run(
        "main:create_app",
        factory=True,
        host=settings.host,
        port=settings.port,
        reload=True
    )
