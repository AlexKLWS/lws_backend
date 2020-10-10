from fastapi import APIRouter

from lws_backend.api.routes import articles, previews, ext_material

router = APIRouter()

router.include_router(articles.router, tags=["articles"], prefix="/articles")
router.include_router(previews.router, tags=["previews"], prefix="/previews")
router.include_router(ext_material.router, tags=["ext_materials"], prefix="/ext-materials")
