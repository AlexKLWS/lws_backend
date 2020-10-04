from fastapi import APIRouter, Depends, HTTPException

from lws_backend.database import Session, get_db
from lws_backend.database_models.articles import Article
from lws_backend.crud.articles import get_article_by_id

api_router = APIRouter()


@api_router.get("/articles")
async def get_article(id: str, db: Session = Depends(get_db)):
    article = get_article_by_id(id, db)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
