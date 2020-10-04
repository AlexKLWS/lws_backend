from sqlalchemy import and_

from lws_backend.pydantic_models.category import Category
from lws_backend.database_models.page_index import PageIndex
from lws_backend.database import Session


def get_page_index(db: Session, pageNumber: int, category: Category):
    return db.query(PageIndex).filter(and_(PageIndex.page == pageNumber, PageIndex.category == category.value)).first()


def get_pages_count(db: Session, category: Category):
    return db.query(PageIndex).filter(PageIndex.category == category.value).count()
