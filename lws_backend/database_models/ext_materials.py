from sqlalchemy import Column, ForeignKey, Integer, String, Table, Boolean
from sqlalchemy.orm import relationship

from lws_backend.database import Base
from lws_backend.database_models.base import DatabaseBaseModel
from lws_backend.database_models.category import Category
from lws_backend.database_models.icons import Icon
from lws_backend.pydantic_models.ext_material import ExtMaterial as ExtMaterialJsonified


ext_materials_category_association = Table('ext_materials_category_association', Base.metadata,
                                           Column('ext_materials_id', Integer, ForeignKey('ext_materials.id')),
                                           Column('category_id', Integer, ForeignKey('categories.id'))
                                           )


class ExtMaterial(DatabaseBaseModel):
    __tablename__ = "ext_materials"

    reference_id = Column(String, nullable=False)
    name = Column(String)
    subtitle = Column(String)
    hidden = Column(Boolean)
    url = Column(String)
    icon_id = Column(Integer, ForeignKey("icons.id"))

    categories = relationship(
        Category,
        secondary=ext_materials_category_association,
        back_populates="ext_materials")
    icon = relationship(Icon, lazy="joined")

    def get_jsonified_dict(self):
        return {
            "createdAt": self.created_at,
            "referenceId": self.reference_id,
            "name": self.name,
            "subtitle": self.subtitle,
            "hidden": self.hidden,
            "url": self.url,
            "icon": self.icon.get_jsonified_dict()
        }

    def from_jsonified_dict(self, e: ExtMaterialJsonified):
        self.reference_id = e.referenceId
        self.name = e.name
        self.subtitle = e.subtitle
        self.category = e.category
        self.url = e.url
        if e.createdAt is not None:
            self.created_at = e.createdAt
        return self
