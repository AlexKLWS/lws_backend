from fastapi import APIRouter, Depends, HTTPException, status
import uuid

from lws_backend.database import Session, get_managed_session
from lws_backend.crud.ext_materials import get_ext_material_by_id, upsert_ext_material
from lws_backend.pydantic_models.ext_material import ExtMaterial
from lws_backend.pydantic_models.category import Category
from lws_backend.api.dependencies.authorization import check_user_auth
from lws_backend.pydantic_models.user_access_rights import UserAccessRights
from lws_backend.crud.page_index import update_index
from lws_backend.core.update_client_snap import ClientSnapUpdater

router = APIRouter()


@router.get("", response_model=ExtMaterial)
async def get_ext_material(id: str, db: Session = Depends(get_managed_session),
                           user_auth=Depends(check_user_auth)):
    ext_material = get_ext_material_by_id(db, id)

    if ext_material is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="External material not found")

    if ext_material.hidden:
        exception = user_auth[1]
        if exception:
            raise exception
        access_rights = user_auth[0]
        if access_rights != UserAccessRights.READ and access_rights != UserAccessRights.WRITE:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User doesn't have required access rights")

    ext_material_response = ext_material.get_jsonified_dict()

    return ext_material_response


@router.post("", response_model=ExtMaterial)
async def add_or_update_ext_material(ext_material: ExtMaterial, db: Session = Depends(get_managed_session),
                                     user_auth=Depends(check_user_auth)):
    exception = user_auth[1]
    if exception:
        raise exception
    access_rights = user_auth[0]
    if access_rights != UserAccessRights.WRITE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't have required access rights")
    if ext_material.referenceId is None:
        ext_material.referenceId = str(uuid.uuid4())
    ext_material.categories.append(Category.MISC)
    # Removing duplicates
    ext_material.categories = list(dict.fromkeys(ext_material.categories))

    upsert_ext_material(db, ext_material)
    update_index(db, ext_material.categories)
    updater = ClientSnapUpdater.get_or_create_updater()
    updater.update()

    return ext_material
