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

    def get_jsonified_dict(self):
        return {
            "createdAt": self.created_at,
            "referenceId": self.reference_id,
            "name": self.name,
            "subtitle": self.subtitle,
            "category": self.category,
        }


class Article(ArticleBase):
    article_text = Column(Text)

    def get_jsonified_dict(self):
        transferable = super().get_jsonified_dict()
        transferable["articleText"] = self.article_text
        return transferable


class ArticlePreview(ArticleBase):
    icon_id = Column(Integer, ForeignKey("icons.id"))

    icon = relationship(Icon, lazy="joined")

    def get_jsonified_dict(self):
        transferable = super().get_jsonified_dict()
        transferable["icon"] = self.icon.get_jsonified_dict()
        return transferable
