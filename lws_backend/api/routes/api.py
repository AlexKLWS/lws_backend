from fastapi import APIRouter

from lws_backend.api.routes import articles, previews, ext_materials, login, files, guides, auth

router = APIRouter()

router.include_router(articles.router, tags=["articles"], prefix="/articles")
router.include_router(previews.router, tags=["previews"], prefix="/previews")
router.include_router(ext_materials.router, tags=["ext_materials"], prefix="/ext-materials")
router.include_router(guides.router, tags=["guides"], prefix="/guides")
router.include_router(login.router, tags=["login"], prefix="/login")
router.include_router(files.router, tags=["files"], prefix="/files")
router.include_router(auth.router, tags=["auth"], prefix="/auth")
