from fastapi import APIRouter, Depends, HTTPException, status
import uuid

from lws_backend.database import Session, get_db
from lws_backend.pydantic_models.guide import Guide
from lws_backend.crud.guides import get_guide_by_id, upsert_guide
from lws_backend.pydantic_models.category import Category
from lws_backend.api.dependencies.authorization import check_user_auth
from lws_backend.pydantic_models.user_access_rights import UserAccessRights
from lws_backend.crud.page_index import update_index

router = APIRouter()


@router.get("", response_model=Guide)
async def get_guide(id: str, db: Session = Depends(get_db),
                    user_auth=Depends(check_user_auth)):
    guide = get_guide_by_id(db, id)

    if guide is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guide not found")

    if guide.hidden:
        exception = user_auth[1]
        if exception:
            raise exception
        access_rights = user_auth[0]
        if access_rights != UserAccessRights.READ and access_rights != UserAccessRights.WRITE:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User doesn't have required access rights")

    guide_response = guide.get_jsonified_dict()

    return guide_response


@router.post("", response_model=Guide)
async def add_or_update_guide(guide: Guide, db: Session = Depends(get_db),
                              user_auth=Depends(check_user_auth)):
    exception = user_auth[1]
    if exception:
        raise exception
    access_rights = user_auth[0]
    if access_rights != UserAccessRights.WRITE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't have required access rights")

    if not guide.referenceId:
        guide.referenceId = str(uuid.uuid4())
    guide.categories.append(Category.MISC)
    # Removing duplicates
    guide.categories = list(dict.fromkeys(guide.categories))

    for location in guide.locations:
        if not location.referenceId:
            location.referenceId = str(uuid.uuid4())

    upsert_guide(db, guide)
    update_index(db, guide.categories)

    return guide
