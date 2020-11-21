from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status

from lws_backend.database import Session, get_managed_session
from lws_backend.pydantic_models.category import Category
from lws_backend.api.dependencies.authorization import check_user_auth
from lws_backend.crud.page_index import get_page_index, get_pages_count
from lws_backend.crud.articles import get_article_previews
from lws_backend.crud.ext_materials import get_ext_material_previews
from lws_backend.pydantic_models.user_access_rights import UserAccessRights
from lws_backend.crud.guides import get_guide_previews
from lws_backend.pydantic_models.preview import PreviewResponse

router = APIRouter()


@router.get("", response_model=PreviewResponse)
async def get_previews(
        category: Category, page: int = 1, include_hidden: Optional[bool] = False,
        db: Session = Depends(get_managed_session), user_auth=Depends(check_user_auth)):

    if include_hidden:
        exception = user_auth[1]
        if exception:
            raise exception
        access_rights = user_auth[0]
        if access_rights != UserAccessRights.READ and access_rights != UserAccessRights.WRITE:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User doesn't have required access rights")

    page_index = get_page_index(db, page, category)
    if page_index is None:
        return {"previews": [], "pageCount": 1}

    page_count = get_pages_count(db, category)

    previews = []
    article_previews = get_article_previews(db, page_index, category, include_hidden)
    for p in article_previews:
        previews.append(p.get_jsonified_dict())

    ext_materials_previews = get_ext_material_previews(db, page_index, category, include_hidden)
    for p in ext_materials_previews:
        previews.append(p.get_jsonified_dict())

    guide_previews = get_guide_previews(db, page_index, category, include_hidden)
    for g in guide_previews:
        previews.append(g.get_jsonified_dict())

    previews.sort(key=lambda p: p["createdAt"], reverse=True)

    return {"previews": previews, "pageCount": page_count}
