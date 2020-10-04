from typing import Tuple, Callable
from fastapi import FastAPI

from lws_backend.core.config import (
    Config,
    VERSION,
    IS_DEBUG,
    DB_CONNECTION_URI,
    API_PREFIX,
)
from lws_backend.mounts.frontend import frontend
from lws_backend.database import prepare_database
from lws_backend.api.routes.articles import api_router as article_router


def get_application() -> Tuple[FastAPI, Config]:
    config = Config(__file__)
    config.setup()

    prepare_database(config.get(DB_CONNECTION_URI))

    main = FastAPI(version=config.get(VERSION), debug=config.get(IS_DEBUG))
    main.include_router(article_router, prefix=API_PREFIX)
    main.mount("/", app=frontend)

    return main, config


app, config = get_application()
