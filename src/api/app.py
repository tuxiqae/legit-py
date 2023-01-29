from typing import Dict

import uvicorn
from fastapi import FastAPI

from utils import logs
from utils.settings import Settings

from .routers import realms


def _get_app_config() -> Dict[str, str | list[str]]:
    description = """
Our API helps you do awesome stuff. 🚀


## Realms 

You will be able to:

* **Create realm**
    POST /realms/create
"""
    conf = {
        "title": "KeyCloak Realm Creator",
        "description": description,
        "version": "0.1.0",
        "docs_url": "/doc",
        "redoc_url": "/redoc",
        "openapi_tags": [{"name": "realm", "description": "Creates KeyCloak realms"}],
        "license": {"name": "MIT", "url": "https://mit-license.org/"},
    }
    return conf


def get_app(settings: Settings) -> FastAPI:
    conf = _get_app_config()
    app = FastAPI(**conf)
    app.state.settings = settings
    app.include_router(realms.realm_router)

    return app


def init_app(app: FastAPI, *args, **kwargs) -> None:
    settings = app.state.settings
    logs.logger.info("Starting the webapp! 🚀")
    uvicorn.run(app, host=str(settings.address), port=settings.port, *args, **kwargs)
    logs.logger.info("Shutting down...")
