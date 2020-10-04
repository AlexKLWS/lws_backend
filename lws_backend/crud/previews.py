from sqlalchemy import and_

from lws_backend.database import Session
from lws_backend.database_models.articles import ArticlePreview
from lws_backend.database_models.ext_material import ExtMaterialPreview
from lws_backend.database_models.page_index import PageIndex
from lws_backend.pydantic_models.category import Category


def get_previews(db: Session, page_index: PageIndex, category: Category):
    article_preview_filter = None
    if page_index.page == 1:
        article_preview_filter = and_(ArticlePreview.created_at >= page_index.end_date, ArticlePreview.category ==
                                      category.value) if category != Category.MISC else and_(ArticlePreview.created_at >= page_index.end_date)
    else:
        article_preview_filter = and_(ArticlePreview.created_at >= page_index.end_date, ArticlePreview.created_at <= page_index.start_date, ArticlePreview.category ==
                                      category.value) if category != Category.MISC else and_(ArticlePreview.created_at >= page_index.end_date, ArticlePreview.created_at <= page_index.start_date)

    if article_preview_filter is not None:
        article_previews = db.query(
            ArticlePreview).filter(article_preview_filter).all()
        return article_previews
    return None
