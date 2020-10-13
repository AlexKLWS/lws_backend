from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lws_backend.database_models.base import DatabaseBaseModel
from lws_backend.database_models.icons import Icon
from lws_backend.pydantic_models.ext_materials import ExtMaterial as ExtMaterialJsonified


class ExtMaterial(DatabaseBaseModel):
    __tablename__ = "ext_materials"

    reference_id = Column(String, nullable=False)
    name = Column(String)
    subtitle = Column(String)
    category = Column(Integer, default=0)
    url = Column(String)
    icon_id = Column(Integer, ForeignKey("icons.id"))

    icon = relationship(Icon, lazy="joined")

    def get_jsonified_dict(self):
        return {
            "createdAt": self.created_at,
            "referenceId": self.reference_id,
            "name": self.name,
            "subtitle": self.subtitle,
            "category": self.category,
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
        if e.icon is not None:
            self.icon = Icon().from_jsonified_dict(e.icon)
        return self
