from sqlalchemy import Column, ForeignKey, Integer, String, Text, Table, Boolean
from sqlalchemy.orm import relationship

from lws_backend.database import Base
from lws_backend.database_models.base import DatabaseBaseModel
from lws_backend.database_models.icons import Icon
from lws_backend.pydantic_models.article import Article as ArticleJsonified

"""
My first idea was to create another abstract superclass, that would have categories
as a prop, and then employ a so-called "generic foreign key" approach
to connect this table to categories.
However, this approach is not in line with SQLAlchemy's usual style, as foregoing
foreign key integrity means that the tables can easily contain invalid
references and also have no ability to use in-database cascade functionality.
So I had decided to go with "table_per_association" approach.
"""

articles_category_association = Table('articles_category_association', Base.metadata,
                                      Column('articles_id', Integer, ForeignKey('articles.id')),
                                      Column('category_id', Integer, ForeignKey('categories.id'))
                                      )


class ArticleBase(DatabaseBaseModel):
    __tablename__ = "articles"

    reference_id = Column(String, nullable=False)
    name = Column(String)
    subtitle = Column(String)
    category = Column(Integer, default=0)
    hidden = Column(Boolean)

    categories = relationship(
        "Category",
        secondary=articles_category_association,
        back_populates="articles")

    def get_jsonified_dict(self):
        return {
            "createdAt": self.created_at,
            "referenceId": self.reference_id,
            "name": self.name,
            "subtitle": self.subtitle,
            "categories": [category.enum_value for category in self.categories],
            "hidden": self.hidden,
        }

    def from_jsonified_dict(self, a: ArticleJsonified):
        self.reference_id = a.referenceId
        self.name = a.name
        self.subtitle = a.subtitle
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
