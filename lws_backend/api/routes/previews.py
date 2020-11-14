from fastapi import APIRouter, Depends

from lws_backend.database import Session, get_db
from lws_backend.pydantic_models.category import Category
from lws_backend.crud.page_index import get_page_index, get_pages_count
from lws_backend.crud.articles import get_article_previews
from lws_backend.crud.ext_materials import get_ext_material_previews
from lws_backend.crud.guides import get_guide_previews
from lws_backend.pydantic_models.preview import PreviewResponse

router = APIRouter()


@router.get("", response_model=PreviewResponse)
async def get_previews(
    category: Category, page: int = 1, db: Session = Depends(get_db)
):
    page_index = get_page_index(db, page, category)
    if page_index is None:
        return {"previews": [], "pageCount": 1}

    page_count = get_pages_count(db, category)

    previews = []
    article_previews = get_article_previews(db, page_index, category)
    for p in article_previews:
        previews.append(p.get_jsonified_dict())

    ext_materials_previews = get_ext_material_previews(db, page_index, category)
    for p in ext_materials_previews:
        previews.append(p.get_jsonified_dict())

    guide_previews = get_guide_previews(db, page_index, category)
    for g in guide_previews:
        previews.append(g.get_jsonified_dict())

    previews.sort(key=lambda p: p["createdAt"], reverse=True)

    return {"previews": previews, "pageCount": page_count}
