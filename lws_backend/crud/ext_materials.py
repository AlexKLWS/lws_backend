from typing import List
from sqlalchemy import and_

from lws_backend.database import Session
from lws_backend.pydantic_models.category import Category
from lws_backend.database_models.page_index import PageIndex
from lws_backend.database_models.ext_materials import ExtMaterial
from lws_backend.database_models.icons import Icon
from lws_backend.pydantic_models.ext_materials import ExtMaterial as ExtMaterialJsonified


def get_ext_material_by_id(db: Session, id: str) -> ExtMaterial:
    return db.query(ExtMaterial).filter(ExtMaterial.reference_id == id).first()


def get_ext_material_previews(
    db: Session, page_index: PageIndex, category: Category
) -> List[ExtMaterial]:
    ext_material_preview_filter = None
    if page_index.page == 1:
        ext_material_preview_filter = (
            and_(
                ExtMaterial.created_at >= page_index.end_date,
                ExtMaterial.category == category.value,
            )
            if category != Category.MISC
            else and_(ExtMaterial.created_at >= page_index.end_date)
        )
    else:
        ext_material_preview_filter = (
            and_(
                ExtMaterial.created_at >= page_index.end_date,
                ExtMaterial.created_at <= page_index.start_date,
                ExtMaterial.category == category.value,
            )
            if category != Category.MISC
            else and_(
                ExtMaterial.created_at >= page_index.end_date,
                ExtMaterial.created_at <= page_index.start_date,
            )
        )

    if ext_material_preview_filter is not None:
        ext_material_previews = (
            db.query(ExtMaterial).filter(ext_material_preview_filter).all()
        )
        return ext_material_previews
    return []


def upsert_ext_material(db: Session, ext_material_jsonified: ExtMaterialJsonified):
    try:
        existing_record = db.query(ExtMaterial).filter(ExtMaterial.reference_id ==
                                                       ext_material_jsonified.referenceId).first()
        if existing_record is not None:
            existing_record.from_jsonified_dict(ext_material_jsonified)
            existing_icon_record = db.query(Icon).filter(Icon.id ==
                                                         existing_record.icon_id).first()
            existing_icon_record.from_jsonified_dict(ext_material_jsonified.icon)
        else:
            ext_material = ExtMaterial().from_jsonified_dict(ext_material_jsonified)
            ext_material.icon = Icon().from_jsonified_dict(ext_material_jsonified.icon)
            db.add(ext_material)
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
