from fastapi import APIRouter, Depends, HTTPException, status
import uuid

from lws_backend.database import Session, get_managed_session
from lws_backend.crud.articles import get_article_by_id
from lws_backend.pydantic_models.article import Article
from lws_backend.pydantic_models.category import Category
from lws_backend.api.dependencies.authorization import check_user_auth
from lws_backend.crud.articles import upsert_article
from lws_backend.pydantic_models.user_access_rights import UserAccessRights
from lws_backend.crud.page_index import update_index
from lws_backend.core.update_client_snap import ClientSnapUpdater

router = APIRouter()


@router.get("", response_model=Article)
async def get_article(id: str, db: Session = Depends(get_managed_session),
                      user_auth=Depends(check_user_auth)):
    article = get_article_by_id(db, id)

    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    if article.hidden:
        exception = user_auth[1]
        if exception:
            raise exception
        access_rights = user_auth[0]
        if access_rights != UserAccessRights.READ and access_rights != UserAccessRights.WRITE:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User doesn't have required access rights")

    article_response = article.get_jsonified_dict()

    return article_response


@router.post("", response_model=Article)
async def add_or_update_article(article: Article, db: Session = Depends(get_managed_session),
                                user_auth=Depends(check_user_auth)):
    exception = user_auth[1]
    if exception:
        raise exception
    access_rights = user_auth[0]
    if access_rights != UserAccessRights.WRITE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't have required access rights")

    if article.referenceId is None:
        article.referenceId = str(uuid.uuid4())
    article.categories.append(Category.MISC)
    # Removing duplicates
    article.categories = list(dict.fromkeys(article.categories))

    upsert_article(db, article)
    update_index(db, article.categories)
    updater = ClientSnapUpdater.get_or_create_updater()
    updater.update()

    return article
