#!/usr/bin/env python
import uvicorn
from fastapi import FastAPI

from config.settings import settings
from routers.secrets import router as secrets_router


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

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
