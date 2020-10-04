from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

from fastapi_test.database import Base
from fastapi_test.models.icons import Icon


class ArticleBase(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    deleted_at = Column(DateTime(timezone=True))
    reference_id = Column(String, nullable=False)
    name = Column(String)
    subtitle = Column(String)
    category = Column(Integer, default=0)


class Article(ArticleBase):
    article_text = Column(Text)


class ArticlePreview(ArticleBase):
    icon_id = Column(Integer, ForeignKey("icon.id"))

    icon = relationship("Icon", lazy="joined")
