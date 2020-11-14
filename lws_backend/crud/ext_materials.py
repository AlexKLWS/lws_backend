from typing import List
from sqlalchemy import and_

from lws_backend.database import Session
from lws_backend.database_models.categories import Category as DBCategory
from lws_backend.pydantic_models.category import Category
from lws_backend.database_models.page_index import PageIndex
from lws_backend.database_models.ext_materials import ExtMaterial
from lws_backend.database_models.icons import Icon
from lws_backend.pydantic_models.ext_material import ExtMaterial as ExtMaterialJsonified


def get_ext_material_by_id(db: Session, id: str) -> ExtMaterial:
    return db.query(ExtMaterial).filter(ExtMaterial.reference_id == id).first()


def get_ext_material_previews(
    db: Session, page_index: PageIndex, category: Category
) -> List[ExtMaterial]:
    category_record = db.query(DBCategory).filter(DBCategory.enum_value == category.value).first()
    if category_record is None:
        return []
    if page_index.page == 1:
        ext_material_previews = category_record.ext_materials.filter(and_(
            ExtMaterial.created_at >= page_index.start_date,
            ExtMaterial.hidden.isnot(True),
        )).all()
        return ext_material_previews
    else:
        ext_material_previews = category_record.ext_materials.filter(and_(
            ExtMaterial.created_at >= page_index.start_date,
            ExtMaterial.created_at <= page_index.end_date,
            ExtMaterial.hidden.isnot(True),
        )).all()
        return ext_material_previews


def upsert_ext_material(db: Session, ext_material_jsonified: ExtMaterialJsonified):
    categories = []
    for category in ext_material_jsonified.categories:
        category_record = db.query(DBCategory).filter(DBCategory.enum_value == category.value).first()
        if category_record is None:
            category_record = DBCategory(enum_value=category.value)
            db.add(category_record)
        categories.append(category_record)

    existing_record = db.query(ExtMaterial).filter(ExtMaterial.reference_id ==
                                                   ext_material_jsonified.referenceId).first()
    if existing_record is not None:
        existing_record.from_jsonified_dict(ext_material_jsonified)
        existing_record.categories.clear()
        existing_record.categories.extend(categories)
        existing_icon_record = db.query(Icon).filter(Icon.id ==
                                                     existing_record.icon_id).first()
        existing_icon_record.from_jsonified_dict(ext_material_jsonified.icon)

    else:
        ext_material = ExtMaterial().from_jsonified_dict(ext_material_jsonified)
        ext_material.icon = Icon().from_jsonified_dict(ext_material_jsonified.icon)
        ext_material.categories.extend(categories)
        db.add(ext_material)
