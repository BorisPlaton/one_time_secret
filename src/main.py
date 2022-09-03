#!/usr/bin/env python
import asyncio

import uvicorn

from config.settings import settings
from utils.setup import configure_project, create_app


app = create_app()

if __name__ == '__main__':
    asyncio.run(configure_project())
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.development
    )
