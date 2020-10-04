from sqlalchemy import and_

from lws_backend.database import Session
from lws_backend.pydantic_models.category import Category
from lws_backend.database_models.page_index import PageIndex
from lws_backend.database_models.ext_material import ExtMaterialPreview


def get_ext_material_previews(db: Session, page_index: PageIndex, category: Category):
    ext_material_preview_filter = None
    if page_index.page == 1:
        ext_material_preview_filter = and_(ExtMaterialPreview.created_at >= page_index.end_date, ExtMaterialPreview.category ==
                                           category.value) if category != Category.MISC else and_(ExtMaterialPreview.created_at >= page_index.end_date)
    else:
        ext_material_preview_filter = and_(ExtMaterialPreview.created_at >= page_index.end_date, ExtMaterialPreview.created_at <= page_index.start_date, ExtMaterialPreview.category ==
                                           category.value) if category != Category.MISC else and_(ExtMaterialPreview.created_at >= page_index.end_date, ExtMaterialPreview.created_at <= page_index.start_date)

    if ext_material_preview_filter is not None:
        ext_material_previews = db.query(
            ExtMaterialPreview).filter(ext_material_preview_filter).all()
        return ext_material_previews
    return []
