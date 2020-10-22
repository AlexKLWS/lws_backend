import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lws_backend.core.config import (
    VERSION,
    IS_DEBUG,
    DB_CONNECTION_URI,
    API_PREFIX,
    ASSETS_PREFIX,
    ASSETS_PATH,
    CLIENT_PATH
)
from lws_backend.database import prepare_database
from lws_backend.api.routes import api
from lws_backend.config import config
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

origins = [
    "http://localhost:3000",
]


def get_application() -> FastAPI:
    prepare_database(config.get(DB_CONNECTION_URI))

    main = FastAPI(version=config.get(VERSION), debug=config.get(IS_DEBUG))
    main.include_router(api.router, prefix=API_PREFIX)

    main.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                        allow_methods=["*"], allow_headers=["*"],)

    if not os.path.exists(ASSETS_PATH):
        os.mkdir(ASSETS_PATH)
    main.mount(ASSETS_PREFIX, StaticFiles(directory=ASSETS_PATH))

    if not os.path.exists(CLIENT_PATH):
        os.mkdir(CLIENT_PATH)
    main.mount("/", StaticFiles(directory=CLIENT_PATH))

    return main


app = get_application()


@app.middleware("http")
async def redirect_to_index(request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return FileResponse(os.path.join(CLIENT_PATH, "index.html"))
    return response
