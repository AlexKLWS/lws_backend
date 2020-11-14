from fastapi import APIRouter, Depends, HTTPException, status
import uuid

from lws_backend.database import Session, get_db
from lws_backend.crud.managed_session import managed_session
from lws_backend.pydantic_models.guide import Guide
from lws_backend.crud.guides import get_guide_by_id, upsert_guide
from lws_backend.pydantic_models.category import Category
from lws_backend.api.dependencies.authorization import check_user_auth
from lws_backend.pydantic_models.user_access_rights import UserAccessRights
from lws_backend.crud.page_index import update_index

router = APIRouter()


@router.get("", response_model=Guide)
async def get_guide(id: str, db: Session = Depends(get_db)):
    with managed_session(db) as session:
        guide = get_guide_by_id(session, id)

    if guide is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guide not found")

    return guide.get_jsonified_dict()


@router.post("", response_model=Guide)
async def add_or_update_guide(guide: Guide, db: Session = Depends(get_db),
                              access_rights=Depends(check_user_auth)):
    if access_rights != UserAccessRights.WRITE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't have required access rights")

    if not guide.referenceId:
        guide.referenceId = str(uuid.uuid4())
    guide.categories.append(Category.MISC)

    for location in guide.locations:
        if not location.referenceId:
            location.referenceId = str(uuid.uuid4())

    with managed_session(db) as session:
        upsert_guide(session, guide)
        update_index(session, guide.categories)

    return guide
