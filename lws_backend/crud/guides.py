from typing import List
from sqlalchemy import and_

from lws_backend.database import Session
from lws_backend.database_models.categories import Category
from lws_backend.pydantic_models.category import Category as CategoryENUM
from lws_backend.database_models.guides import Guide, GuidePreview, GuideLocationInfo
from lws_backend.database_models.icons import Icon
from lws_backend.database_models.page_index import PageIndex
from lws_backend.pydantic_models.guide import Guide as GuideJsonified


def get_guide_by_id(db: Session, id: str) -> Guide:
    return db.query(Guide).filter_by(reference_id=id).first()


def get_guide_previews(
    db: Session, page_index: PageIndex, category: CategoryENUM, include_hidden: bool,
) -> List[GuidePreview]:
    category_record = db.query(Category).filter_by(enum_value=category.value).first()
    if category_record is None:
        return []
    if include_hidden:
        if page_index.page == 1:
            guide_previews = category_record.guides.filter(GuidePreview.created_at >= page_index.start_date).all()
            return guide_previews
        else:
            guide_previews = category_record.guides.filter(
                and_(GuidePreview.created_at >= page_index.start_date,
                     GuidePreview.created_at <= page_index.end_date)).all()
            return guide_previews
    else:
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
    for category in guide_jsonified.categories:
        category_record = db.query(Category).filter_by(enum_value=category.value).first()
        if category_record is None:
            category_record = Category(enum_value=category.value)
            db.add(category_record)
        categories.append(category_record)

    existing_record = db.query(Guide).filter_by(reference_id=guide_jsonified.referenceId).first()
    if existing_record is not None:
        existing_record.from_jsonified_dict(guide_jsonified)
        existing_record.categories.clear()
        existing_record.categories.extend(categories)
        existing_record.locations.clear()
        existing_record.locations = [GuideLocationInfo().from_jsonified_dict(location)
                                     for location in guide_jsonified.locations]
        existing_icon_record = db.query(Icon).filter_by(id=existing_record.icon_id).first()
        existing_icon_record.from_jsonified_dict(guide_jsonified.icon)
    else:
        guide = Guide().from_jsonified_dict(guide_jsonified)
        guide.icon = Icon().from_jsonified_dict(guide_jsonified.icon)
        guide.locations = [GuideLocationInfo().from_jsonified_dict(location)
                           for location in guide_jsonified.locations]
        guide.categories.extend(categories)
        db.add(guide)
