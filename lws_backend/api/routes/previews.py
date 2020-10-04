from typing import Optional
from fastapi import APIRouter, Depends, HTTPException

from lws_backend.database import Session, get_db
from lws_backend.pydantic_models.category import Category
from lws_backend.crud.page_index import get_page_index, get_pages_count
from lws_backend.crud.previews import get_previews as get_previews_crud

router = APIRouter()


@router.get("")
async def get_previews(category: Category, page: Optional[int], db: Session = Depends(get_db)):
    c = category
    p = page if page is not None else 1

    page_index = get_page_index(db, p, c)
    page_count = get_pages_count(db, c)
    print(f"Page count {page_count}")

    return get_previews_crud(db, page_index, c)
