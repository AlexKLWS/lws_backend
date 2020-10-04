from lws_backend.database import Session
from lws_backend.database_models.articles import Article


def get_article_by_id(id: str, db: Session):
    return db.query(Article).filter(Article.reference_id == id).first()
