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
async def get_guide(id: str, db: Session = Depends(get_db)):
    guide = get_guide_by_id(db, id)
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

    if guide.category != Category.GUIDES.value:
        guide.category = Category.GUIDES

    for location in guide.locations:
        if not location.referenceId:
            location.referenceId = str(uuid.uuid4())

    upsert_guide(db, guide)
    update_index(db, Category.MISC)
    update_index(db, Category.GUIDES)

    return guide
