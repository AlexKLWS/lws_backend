from fastapi import APIRouter, Depends, HTTPException, status
import uuid

from lws_backend.database import Session, get_db
from lws_backend.crud.articles import get_article_by_id
from lws_backend.pydantic_models.article import Article
from lws_backend.pydantic_models.category import Category
from lws_backend.api.dependencies.authorization import check_user_auth
from lws_backend.crud.articles import upsert_article
from lws_backend.pydantic_models.user_access_rights import UserAccessRights
from lws_backend.crud.page_index import update_index

router = APIRouter()


@router.get("", response_model=Article)
async def get_article(id: str, db: Session = Depends(get_db)):
    article = get_article_by_id(db, id)
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    return article.get_jsonified_dict()


@router.post("", response_model=Article)
async def add_or_update_article(article: Article, db: Session = Depends(get_db),
                                access_rights=Depends(check_user_auth)):
    if access_rights != UserAccessRights.WRITE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't have required access rights")

    if article.referenceId is None:
        article.referenceId = str(uuid.uuid4())
    upsert_article(db, article)

    update_index(db, Category.MISC)
    if article.category != Category.MISC:
        update_index(db, article.category)

    return article
