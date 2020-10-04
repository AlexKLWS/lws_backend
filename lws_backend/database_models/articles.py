from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from lws_backend.database_models.base import DatabaseBaseModel
from lws_backend.database_models.icons import Icon


class ArticleBase(DatabaseBaseModel):
    __tablename__ = "articles"

    reference_id = Column(String, nullable=False)
    name = Column(String)
    subtitle = Column(String)
    category = Column(Integer, default=0)


class Article(ArticleBase):
    article_text = Column(Text)


class ArticlePreview(ArticleBase):
    icon_id = Column(Integer, ForeignKey("icons.id"))

    icon = relationship("Icon", lazy="joined")
