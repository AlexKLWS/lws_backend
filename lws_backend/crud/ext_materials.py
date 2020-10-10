from typing import List
from sqlalchemy import and_

from lws_backend.database import Session
from lws_backend.pydantic_models.category import Category
from lws_backend.database_models.page_index import PageIndex
from lws_backend.database_models.ext_material import ExtMaterial


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
