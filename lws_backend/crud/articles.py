from typing import List
from sqlalchemy import and_

from lws_backend.database import Session
from lws_backend.database_models.categories import Category
from lws_backend.pydantic_models.category import Category as CategoryENUM
from lws_backend.database_models.page_index import PageIndex
from lws_backend.database_models.articles import Article, ArticlePreview
from lws_backend.database_models.icons import Icon
from lws_backend.pydantic_models.article import Article as ArticleJsonified


def get_article_by_id(db: Session, id: str) -> Article:
    return db.query(Article).filter_by(reference_id=id).first()


def get_article_previews(
    db: Session, page_index: PageIndex, category: CategoryENUM, include_hidden: bool,
) -> List[ArticlePreview]:
    category_record = db.query(Category).filter_by(enum_value=category.value).first()
    if category_record is None:
        return []
    if include_hidden:
        if page_index.page == 1:
            article_previews = category_record.articles.filter(ArticlePreview.created_at >= page_index.start_date
                                                               ).all()
            return article_previews
        else:
            article_previews = category_record.articles.filter(and_(ArticlePreview.created_at >= page_index.start_date,
                                                                    ArticlePreview.created_at <= page_index.end_date
                                                                    )).all()
            return article_previews
    else:
        if page_index.page == 1:
            article_previews = category_record.articles.filter(
                and_(ArticlePreview.created_at >= page_index.start_date, ArticlePreview.hidden.isnot(True))).all()
            return article_previews
        else:
            article_previews = category_record.articles.filter(and_(ArticlePreview.created_at >= page_index.start_date,
                                                                    ArticlePreview.created_at <= page_index.end_date,
                                                                    ArticlePreview.hidden.isnot(True))).all()
            return article_previews


def upsert_article(db: Session, article_jsonified: ArticleJsonified):
    categories = []
    for category in article_jsonified.categories:
        category_record = db.query(Category).filter_by(enum_value=category.value).first()
        if category_record is None:
            category_record = Category(enum_value=category.value)
            db.add(category_record)
        categories.append(category_record)

    existing_record = db.query(Article).filter_by(reference_id=article_jsonified.referenceId).first()
    if existing_record is not None:
        existing_record.from_jsonified_dict(article_jsonified)
        existing_record.categories.clear()
        existing_record.categories.extend(categories)
        existing_icon_record = db.query(Icon).filter_by(id=existing_record.icon_id).first()
        existing_icon_record.from_jsonified_dict(article_jsonified.icon)
    else:
        article = Article().from_jsonified_dict(article_jsonified)
        article.icon = Icon().from_jsonified_dict(article_jsonified.icon)
        article.categories.extend(categories)
        db.add(article)
