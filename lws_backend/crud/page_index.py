from typing import List
from sqlalchemy import and_

from lws_backend.database_models.categories import Category
from lws_backend.pydantic_models.category import Category as CategoryENUM
from lws_backend.database_models.page_index import PageIndex
from lws_backend.database_models.articles import Article
from lws_backend.database_models.guides import Guide
from lws_backend.database_models.ext_materials import ExtMaterial
from lws_backend.config import config
from lws_backend.core.config import PAGE_SIZE
from lws_backend.database import Session


def get_page_index(db: Session, pageNumber: int, category: CategoryENUM) -> PageIndex:
    category_record = db.query(Category).filter_by(enum_value=category.value).first()
    if category_record is None:
        return None
    return (
        db.query(PageIndex)
        .filter(
            and_(PageIndex.page == pageNumber, PageIndex.category_id == category_record.id)
        )
        .first()
    )


def get_pages_count(db: Session, category: CategoryENUM) -> int:
    category_record = db.query(Category).filter_by(enum_value=category.value).first()
    if category_record is None:
        return 1
    return db.query(PageIndex).filter(PageIndex.category_id == category_record.id).count()


def update_index(db: Session, categories: List[CategoryENUM]):
    for category in categories:
        all_materials = []
        category_record = db.query(Category).filter_by(enum_value=category.value).first()
        articles = category_record.articles.filter(Article.hidden.isnot(True), Article.secret.isnot(True))
        for a in articles:
            all_materials.append(a)

        ext_materials = category_record.ext_materials.filter(ExtMaterial.hidden.isnot(True),
                                                             ExtMaterial.secret.isnot(True))
        for e in ext_materials:
            all_materials.append(e)

        guides = category_record.guides.filter(Guide.hidden.isnot(True), Guide.secret.isnot(True))
        for g in guides:
            all_materials.append(g)

        all_materials.sort(key=lambda m: m.created_at, reverse=True)

        page_size = config.get(PAGE_SIZE)

        page = 1
        if len(all_materials) <= page_size:
            start_date = all_materials[-1].created_at
            end_date = all_materials[0].created_at
            existing_record = db.query(PageIndex).filter(
                and_(PageIndex.page == page, PageIndex.category_id == category_record.id)).first()
            if existing_record is not None:
                existing_record.start_date = start_date
                existing_record.end_date = end_date
            else:
                index = PageIndex(start_date=start_date, end_date=end_date, page=page, category=category_record)
                db.add(index)
        else:
            while len(all_materials) > 0:
                current_page_size = page_size if len(all_materials) > page_size else len(all_materials)
                page_materials = all_materials[:current_page_size]
                del all_materials[:current_page_size]
                start_date = page_materials[-1].created_at
                end_date = page_materials[0].created_at
                existing_record = db.query(PageIndex).filter(
                    and_(PageIndex.page == page, PageIndex.category_id == category_record.id)).first()
                if existing_record is not None:
                    existing_record.start_date = start_date
                    existing_record.end_date = end_date
                else:
                    index = PageIndex(start_date=start_date, end_date=end_date, page=page, category=category_record)
                    db.add(index)

                page += 1
