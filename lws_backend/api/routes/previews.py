from fastapi import APIRouter, Depends

from lws_backend.database import Session, get_db
from lws_backend.pydantic_models.category import Category
from lws_backend.crud.page_index import get_page_index, get_pages_count
from lws_backend.crud.articles import get_article_previews
from lws_backend.crud.ext_materials import get_ext_material_previews

router = APIRouter()


@router.get("")
async def get_previews(
    category: Category, page: int = 1, db: Session = Depends(get_db)
):
    page_index = get_page_index(db, page, category)
    page_count = get_pages_count(db, category)

    previews = []
    article_previews = get_article_previews(db, page_index, category)
    for p in article_previews:
        previews.append(p.get_transferable())

    ext_materials_previews = get_ext_material_previews(db, page_index, category)
    for p in ext_materials_previews:
        previews.append(p.get_transferable())

    previews.sort(key=lambda p: p["createdAt"], reverse=True)

    return {"previews": previews, "page_count": page_count}
