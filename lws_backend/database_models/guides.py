from sqlalchemy import Column, ForeignKey, Integer, Boolean, String, Table, JSON
from sqlalchemy.orm import relationship

from lws_backend.database import Base
from lws_backend.database_models.base import DatabaseBaseModel
from lws_backend.database_models.icons import Icon
from lws_backend.database_models.locations import GuideLocationInfo
from lws_backend.pydantic_models.guide import Guide as GuideJsonified

"""
My first idea was to create another abstract superclass, that would have categories
as a prop, and then employ a so-called "generic foreign key" approach
to connect this table to categories.
However, this approach is not in line with SQLAlchemy's usual style, as foregoing
foreign key integrity means that the tables can easily contain invalid
references and also have no ability to use in-database cascade functionality.
So I had decided to go with "table_per_association" approach.
"""

guides_category_association = Table('guides_category_association', Base.metadata,
                                    Column('guides_id', Integer, ForeignKey('guides.id')),
                                    Column('category_id', Integer, ForeignKey('categories.id'))
                                    )


class GuideBase(DatabaseBaseModel):
    __tablename__ = "guides"

    reference_id = Column(String, nullable=False)
    name = Column(String)
    subtitle = Column(String)
    hidden = Column(Boolean)

    categories = relationship(
        "Category",
        secondary=guides_category_association,
        back_populates="guides")

    def get_jsonified_dict(self):
        return {
            "createdAt": self.created_at,
            "referenceId": self.reference_id,
            "name": self.name,
            "subtitle": self.subtitle,
            "categories": [category.enum_value for category in self.categories],
            "hidden": self.hidden
        }

    def from_jsonified_dict(self, g: GuideJsonified):
        self.reference_id = g.referenceId
        self.name = g.name
        self.subtitle = g.subtitle
        if g.createdAt is not None:
            self.created_at = g.createdAt
        return self


class GuidePreview(GuideBase):
    icon_id = Column(Integer, ForeignKey("icons.id"))

    icon = relationship(Icon, lazy="joined")

    def get_jsonified_dict(self):
        transferable = super().get_jsonified_dict()
        transferable["icon"] = self.icon.get_jsonified_dict()
        return transferable

    def from_jsonified_dict(self, g: GuideJsonified):
        super().from_jsonified_dict(g)
        return self


class Guide(GuidePreview):
    locations = relationship(GuideLocationInfo, lazy="joined")
    default_zoom = Column(Integer)
    default_center = Column(JSON)
    info = Column(String)

    def get_jsonified_dict(self):
        transferable = super().get_jsonified_dict()
        transferable["info"] = self.info
        transferable["defaultZoom"] = self.default_zoom
        transferable["defaultCenter"] = self.default_center
        transferable["locations"] = [location.get_jsonified_dict() for location in self.locations]
        return transferable

    def from_jsonified_dict(self, g: GuideJsonified):
        super().from_jsonified_dict(g)
        self.info = g.info
        self.default_zoom = g.defaultZoom
        self.default_center = g.defaultCenter.get_jsonified_dict()
        return self
