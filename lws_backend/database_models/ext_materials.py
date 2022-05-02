from sqlalchemy import Column, ForeignKey, Integer, String, Table, Boolean
from sqlalchemy.orm import relationship

from lws_backend.database import Base
from lws_backend.database_models.base import DatabaseBaseModel
from lws_backend.database_models.icons import Icon
from lws_backend.pydantic_models.ext_material import ExtMaterial as ExtMaterialJsonified

"""
My first idea was to create another abstract superclass, that would have categories
as a prop, and then employ a so-called "generic foreign key" approach
to connect this table to categories.
However, this approach is not in line with SQLAlchemy's usual style, as foregoing
foreign key integrity means that the tables can easily contain invalid
references and also have no ability to use in-database cascade functionality.
So I had decided to go with "table_per_association" approach.
"""

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
    secret = Column(Boolean)
    url = Column(String)
    icon_id = Column(Integer, ForeignKey("icons.id"))

    categories = relationship(
        "Category",
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
            "secret": self.secret,
            "url": self.url,
            "categories": [category.enum_value for category in self.categories],
            "icon": self.icon.get_jsonified_dict()
        }

    def from_jsonified_dict(self, e: ExtMaterialJsonified):
        self.reference_id = e.referenceId
        self.name = e.name
        self.subtitle = e.subtitle
        self.url = e.url
        self.hidden = e.hidden
        self.secret = e.secret
        if e.createdAt is not None:
            self.created_at = e.createdAt
        return self
