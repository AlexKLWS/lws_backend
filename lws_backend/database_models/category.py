from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from lws_backend.database_models.base import DatabaseBaseModel
from lws_backend.database_models.ext_materials import ExtMaterial, ext_materials_category_association
from lws_backend.database_models.articles import Article, articles_category_association
from lws_backend.database_models.guides import Guide, guides_category_association
from lws_backend.database_models.page_index import PageIndex


class Category(DatabaseBaseModel):
    __tablename__ = "categories"

    enum_value = Column(Integer, default=0)

    page_index = relationship(PageIndex, uselist=False, back_populates="category")

    ext_materials = relationship(
        ExtMaterial,
        secondary=ext_materials_category_association,
        back_populates="categories",
        lazy="dynamic")

    articles = relationship(
        Article,
        secondary=articles_category_association,
        back_populates="categories",
        lazy="dynamic")

    guides = relationship(
        Guide,
        secondary=guides_category_association,
        back_populates="categories",
        lazy="dynamic")
