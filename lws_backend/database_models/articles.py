from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from lws_backend.database_models.base import DatabaseBaseModel
from lws_backend.database_models.icons import Icon
from lws_backend.pydantic_models.article import Article as ArticleJsonified


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

    def from_jsonified_dict(self, a: ArticleJsonified):
        self.reference_id = a.referenceId
        self.name = a.name
        self.subtitle = a.subtitle
        self.category = a.category
        if a.createdAt is not None:
            self.created_at = a.createdAt
        return self


class ArticlePreview(ArticleBase):
    icon_id = Column(Integer, ForeignKey("icons.id"))

    icon = relationship(Icon, lazy="joined")

    def get_jsonified_dict(self):
        transferable = super().get_jsonified_dict()
        transferable["icon"] = self.icon.get_jsonified_dict()
        return transferable

    def from_jsonified_dict(self, a: ArticleJsonified):
        super().from_jsonified_dict(a)
        if a.icon is not None:
            self.icon = Icon().from_jsonified_dict(a.icon)
        return self


class Article(ArticlePreview):
    article_text = Column(Text)

    def get_jsonified_dict(self):
        transferable = super().get_jsonified_dict()
        transferable["articleText"] = self.article_text
        return transferable

    def from_jsonified_dict(self, a: ArticleJsonified):
        super().from_jsonified_dict(a)
        self.article_text = a.articleText
        return self
