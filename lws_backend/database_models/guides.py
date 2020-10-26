from sqlalchemy import Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from lws_backend.database_models.base import DatabaseBaseModel
from lws_backend.database_models.icons import Icon
from lws_backend.database_models.locations import GuideLocationInfo
from lws_backend.pydantic_models.guide import Guide as GuideJsonified


class GuideBase(DatabaseBaseModel):
    __tablename__ = "guides"

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

    def from_jsonified_dict(self, g: GuideJsonified):
        self.reference_id = g.referenceId
        self.name = g.name
        self.subtitle = g.subtitle
        self.category = g.category
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

    def get_jsonified_dict(self):
        transferable = super().get_jsonified_dict()
        transferable["defaultZoom"] = self.default_zoom
        transferable["defaultCenter"] = self.default_center
        transferable["locations"] = [location.get_jsonified_dict() for location in self.locations]
        return transferable

    def from_jsonified_dict(self, g: GuideJsonified):
        super().from_jsonified_dict(g)
        self.default_zoom = g.defaultZoom
        self.default_center = g.defaultCenter.get_jsonified_dict()
        return self