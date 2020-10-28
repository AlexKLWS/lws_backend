from typing import List
from sqlalchemy import and_

from lws_backend.database import Session
from lws_backend.database_models.guides import Guide, GuidePreview, GuideLocationInfo
from lws_backend.database_models.icons import Icon
from lws_backend.database_models.page_index import PageIndex
from lws_backend.pydantic_models.guide import Guide as GuideJsonified


def get_guide_by_id(db: Session, id: str) -> Guide:
    return db.query(Guide).filter(Guide.reference_id == id).first()


def get_guide_previews(
    db: Session, page_index: PageIndex
) -> List[GuidePreview]:
    guide_preview_filter = None
    if page_index.page == 1:
        guide_preview_filter = and_(GuidePreview.created_at >= page_index.start_date)
    else:
        guide_preview_filter = and_(GuidePreview.created_at >= page_index.start_date,
                                    GuidePreview.created_at <= page_index.end_date,)

    if guide_preview_filter is not None:
        guide_previews = (
            db.query(GuidePreview).filter(guide_preview_filter).all()
        )
        return guide_previews
    return []


def upsert_guide(db: Session, guide_jsonified: GuideJsonified):
    try:
        existing_record = db.query(Guide).filter(Guide.reference_id == guide_jsonified.referenceId).first()
        if existing_record is not None:
            existing_record.from_jsonified_dict(guide_jsonified)
            existing_icon_record = db.query(Icon).filter(Icon.id ==
                                                         existing_record.icon_id).first()
            existing_icon_record.from_jsonified_dict(guide_jsonified.icon)
        else:
            guide = Guide().from_jsonified_dict(guide_jsonified)
            guide.icon = Icon().from_jsonified_dict(guide_jsonified.icon)
            guide.locations = [GuideLocationInfo().from_jsonified_dict(location)
                               for location in guide_jsonified.locations]
            db.add(guide)
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
