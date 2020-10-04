from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

frontend = FastAPI()


@frontend.middleware("http")
async def redirect_to_index(request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return FileResponse("client/index.html")
    return response


frontend.mount("/", StaticFiles(directory="client"))
