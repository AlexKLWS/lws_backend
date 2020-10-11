from fastapi import APIRouter, Depends, HTTPException

from lws_backend.database import Session, get_db
from lws_backend.crud.ext_materials import get_ext_material_by_id
from lws_backend.pydantic_models.ext_materials import ExtMaterial

router = APIRouter()


@router.get("", response_model=ExtMaterial)
async def get_ext_material(id: str, db: Session = Depends(get_db)):
    ext_material = get_ext_material_by_id(db, id)
    if ext_material is None:
        raise HTTPException(status_code=404, detail="External material not found")

    return ext_material.get_jsonified_dict()
