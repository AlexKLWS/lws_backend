from typing import List
from sqlalchemy import and_

from lws_backend.database import Session
from lws_backend.pydantic_models.category import Category
from lws_backend.database_models.page_index import PageIndex
from lws_backend.database_models.articles import Article, ArticlePreview
from lws_backend.database_models.icons import Icon
from lws_backend.pydantic_models.article import Article as ArticleJsonified


def get_article_by_id(db: Session, id: str) -> Article:
    return db.query(Article).filter(Article.reference_id == id).first()


def get_article_previews(
    db: Session, page_index: PageIndex, category: Category
) -> List[ArticlePreview]:
    article_preview_filter = None
    if page_index.page == 1:
        article_preview_filter = (
            and_(
                ArticlePreview.created_at >= page_index.start_date,
                ArticlePreview.category == category.value,
            )
            if category != Category.MISC
            else and_(ArticlePreview.created_at >= page_index.start_date)
        )
    else:
        article_preview_filter = (
            and_(
                ArticlePreview.created_at >= page_index.start_date,
                ArticlePreview.created_at <= page_index.end_date,
                ArticlePreview.category == category.value,
            )
            if category != Category.MISC
            else and_(
                ArticlePreview.created_at >= page_index.start_date,
                ArticlePreview.created_at <= page_index.end_date,
            )
        )

    if article_preview_filter is not None:
        article_previews = db.query(ArticlePreview).filter(article_preview_filter).all()
        return article_previews
    return []


def upsert_article(db: Session, article_jsonified: ArticleJsonified):
    try:
        existing_record = db.query(Article).filter(Article.reference_id == article_jsonified.referenceId).first()
        if existing_record is not None:
            existing_record.from_jsonified_dict(article_jsonified)
            existing_icon_record = db.query(Icon).filter(Icon.id ==
                                                         existing_record.icon_id).first()
            existing_icon_record.from_jsonified_dict(article_jsonified.icon)
        else:
            article = Article().from_jsonified_dict(article_jsonified)
            article.icon = Icon().from_jsonified_dict(article_jsonified.icon)
            db.add(article)
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
