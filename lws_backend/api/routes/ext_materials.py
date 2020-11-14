from fastapi import APIRouter, Depends, HTTPException, status
import uuid

from lws_backend.database import Session, get_db
from lws_backend.crud.managed_session import managed_session
from lws_backend.crud.ext_materials import get_ext_material_by_id, upsert_ext_material
from lws_backend.pydantic_models.ext_material import ExtMaterial
from lws_backend.pydantic_models.category import Category
from lws_backend.api.dependencies.authorization import check_user_auth
from lws_backend.pydantic_models.user_access_rights import UserAccessRights
from lws_backend.crud.page_index import update_index

router = APIRouter()


@router.get("", response_model=ExtMaterial)
async def get_ext_material(id: str, db: Session = Depends(get_db)):
    with managed_session(db) as session:
        ext_material = get_ext_material_by_id(session, id)

    if ext_material is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="External material not found")

    return ext_material.get_jsonified_dict()


@router.post("", response_model=ExtMaterial)
async def add_or_update_ext_material(ext_material: ExtMaterial, db: Session = Depends(get_db),
                                     access_rights=Depends(check_user_auth)):
    if access_rights != UserAccessRights.WRITE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't have required access rights")
    if ext_material.referenceId is None:
        ext_material.referenceId = str(uuid.uuid4())
    ext_material.categories.append(Category.MISC)

    with managed_session(db) as session:
        upsert_ext_material(session, ext_material)
        update_index(session, ext_material.categories)

    return ext_material
