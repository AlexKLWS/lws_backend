from fastapi import APIRouter, Depends, HTTPException

from lws_backend.database import Session, get_db
from lws_backend.crud.articles import get_article_by_id

router = APIRouter()


@router.get("")
async def get_article(id: str, db: Session = Depends(get_db)):
    article = get_article_by_id(db, id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")

    return article.get_jsonified_dict()
