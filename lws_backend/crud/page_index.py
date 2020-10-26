from sqlalchemy import and_

from lws_backend.pydantic_models.category import Category
from lws_backend.database_models.page_index import PageIndex
from lws_backend.database_models.articles import Article
from lws_backend.database_models.guides import Guide
from lws_backend.database_models.ext_materials import ExtMaterial
from lws_backend.config import config
from lws_backend.core.config import PAGE_SIZE
from lws_backend.database import Session


def get_page_index(db: Session, pageNumber: int, category: Category) -> PageIndex:
    return (
        db.query(PageIndex)
        .filter(
            and_(PageIndex.page == pageNumber, PageIndex.category == category.value)
        )
        .first()
    )


def get_pages_count(db: Session, category: Category) -> int:
    return db.query(PageIndex).filter(PageIndex.category == category.value).count()


def update_index(db: Session, category: Category):
    all_materials = []
    articles = db.query(Article.id, Article.created_at) if category == Category.MISC else db.query(
        Article.id, Article.created_at).filter(Article.category == category.value)
    for a in articles:
        all_materials.append(a)

    ext_materials = db.query(ExtMaterial.id, ExtMaterial.created_at) if category == Category.MISC else db.query(
        ExtMaterial.id, ExtMaterial.created_at).filter(ExtMaterial.category == category.value)
    for e in ext_materials:
        all_materials.append(e)

    guides = db.query(Guide.id, Guide.created_at)
    for g in guides:
        all_materials.append(g)

    all_materials.sort(key=lambda m: m.created_at, reverse=True)

    page_size = config.get(PAGE_SIZE)

    page = 1
    if len(all_materials) <= page_size:
        start_date = all_materials[-1].created_at
        end_date = all_materials[0].created_at
        existing_record = db.query(PageIndex).filter(
            and_(PageIndex.page == page, PageIndex.category == category.value)).first()
        if existing_record is not None:
            existing_record.start_date = start_date
            existing_record.end_date = end_date
        else:
            index = PageIndex(start_date=start_date, end_date=end_date, page=page, category=category.value)
            db.add(index)
    else:
        while len(all_materials) > 0:
            current_page_size = page_size if len(all_materials) > page_size else len(all_materials)
            page_materials = all_materials[:current_page_size]
            del all_materials[:current_page_size]
            start_date = page_materials[-1].created_at
            end_date = page_materials[0].created_at
            existing_record = db.query(PageIndex).filter(
                and_(PageIndex.page == page, PageIndex.category == category.value)).first()
            if existing_record is not None:
                existing_record.start_date = start_date
                existing_record.end_date = end_date
            else:
                index = PageIndex(start_date=start_date, end_date=end_date, page=page, category=category.value)
                db.add(index)

            page += 1

    db.commit()
