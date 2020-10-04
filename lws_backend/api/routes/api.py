from fastapi import APIRouter

from lws_backend.api.routes import articles, previews

router = APIRouter()

router.include_router(articles.router, tags=["articles"], prefix="/articles")
router.include_router(previews.router, tags=["previews"], prefix="/previews")
