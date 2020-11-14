from typing import List
from sqlalchemy import and_

from lws_backend.database import Session
from lws_backend.database_models.categories import Category as DBCategory
from lws_backend.database_models.guides import Guide, GuidePreview, GuideLocationInfo
from lws_backend.database_models.icons import Icon
from lws_backend.database_models.page_index import PageIndex
from lws_backend.pydantic_models.category import Category
from lws_backend.pydantic_models.guide import Guide as GuideJsonified


def get_guide_by_id(db: Session, id: str) -> Guide:
    return db.query(Guide).filter(Guide.reference_id == id).first()


def get_guide_previews(
    db: Session, page_index: PageIndex, category: Category
) -> List[GuidePreview]:
    category_record = db.query(DBCategory).filter(DBCategory.enum_value == category.value).first()
    if category_record is None:
        return []
    if page_index.page == 1:
        guide_previews = category_record.guides.filter(
            and_(GuidePreview.created_at >= page_index.start_date, GuidePreview.hidden.isnot(True))).all()
        return guide_previews
    else:
        guide_previews = category_record.guides.filter(
            and_(GuidePreview.created_at >= page_index.start_date,
                 GuidePreview.created_at <= page_index.end_date, GuidePreview.hidden.isnot(True))).all()
        return guide_previews


def upsert_guide(db: Session, guide_jsonified: GuideJsonified):
    categories = []
    # Removing duplicates
    consolidated_categories = list(dict.fromkeys(guide_jsonified.categories))
    for category in consolidated_categories:
        category_record = db.query(DBCategory).filter(DBCategory.enum_value == category.value).first()
        if category_record is None:
            category_record = DBCategory(enum_value=category.value)
            db.add(category_record)
        categories.append(category_record)

    existing_record = db.query(Guide).filter(Guide.reference_id == guide_jsonified.referenceId).first()
    if existing_record is not None:
        existing_record.from_jsonified_dict(guide_jsonified)
        existing_record.categories.clear()
        existing_record.categories.extend(categories)
        existing_icon_record = db.query(Icon).filter(Icon.id ==
                                                     existing_record.icon_id).first()
        existing_icon_record.from_jsonified_dict(guide_jsonified.icon)
    else:
        guide = Guide().from_jsonified_dict(guide_jsonified)
        guide.icon = Icon().from_jsonified_dict(guide_jsonified.icon)
        guide.locations = [GuideLocationInfo().from_jsonified_dict(location)
                           for location in guide_jsonified.locations]
        guide.categories.extend(categories)
        db.add(guide)
