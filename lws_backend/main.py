import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from lws_backend.core.config import (
    VERSION,
    IS_DEBUG,
    DB_CONNECTION_URI,
    API_PREFIX,
    ASSETS_PREFIX,
    ASSETS_PATH
)
from lws_backend.database import prepare_database
from lws_backend.api.routes import api
from lws_backend.config import config

origins = [
    "http://localhost:3000"
]


def get_application() -> FastAPI:
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG if config.get(IS_DEBUG) else logging.INFO,
                        datefmt="%H:%M:%S")
    prepare_database(config.get(DB_CONNECTION_URI))

    if config.get(IS_DEBUG):
        main = FastAPI(version=config.get(VERSION), debug=True)
    else:
        main = FastAPI(version=config.get(VERSION), debug=False, docs_url=None, redoc_url=None, openapi_url=None)

    main.include_router(api.router, prefix=API_PREFIX)

    main.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                        allow_methods=["*"], allow_headers=["*"],)

    if not os.path.exists(ASSETS_PATH):
        os.mkdir(ASSETS_PATH)
        os.chmod(ASSETS_PATH, 0o755)
    main.mount(ASSETS_PREFIX, StaticFiles(directory=ASSETS_PATH))

    return main


app = get_application()
