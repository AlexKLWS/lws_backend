from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lws_backend.core.config import (
    VERSION,
    IS_DEBUG,
    DB_CONNECTION_URI,
    API_PREFIX,
)
from lws_backend.database import prepare_database
from lws_backend.api.routes import api
from lws_backend.config import config

origins = [
    "http://localhost:3000",
]


def get_application() -> FastAPI:
    prepare_database(config.get(DB_CONNECTION_URI))

    main = FastAPI(version=config.get(VERSION), debug=config.get(IS_DEBUG))
    main.include_router(api.router, prefix=API_PREFIX)

    main.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                        allow_methods=["*"], allow_headers=["*"],)

    return main


app = get_application()
