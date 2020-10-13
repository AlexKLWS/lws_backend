from fastapi import APIRouter, Depends, HTTPException
import uuid

from lws_backend.database import Session, get_db
from lws_backend.crud.articles import get_article_by_id
from lws_backend.pydantic_models.article import Article
from lws_backend.api.dependencies.authorization import check_user_auth
from lws_backend.crud.articles import upsert_article

router = APIRouter()


@router.get("", response_model=Article)
async def get_article(id: str, db: Session = Depends(get_db)):
    article = get_article_by_id(db, id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")

    return article.get_jsonified_dict()


@router.post("")
async def add_or_update_article(article: Article, db: Session = Depends(get_db)):
    if article.referenceId is None:
        article.referenceId = str(uuid.uuid4())
    upsert_article(db, article)
