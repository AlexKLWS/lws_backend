from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lws_backend.database_models.base import DatabaseBaseModel
from lws_backend.database_models.icons import Icon


class ExtMaterialBase(DatabaseBaseModel):
    __tablename__ = "ext_materials"

    reference_id = Column(String, nullable=False)
    name = Column(String)
    subtitle = Column(String)
    category = Column(Integer, default=0)
    url = Column(String)

    def get_transferable(self):
        return {
            "createdAt": self.created_at,
            "referenceId": self.reference_id,
            "name": self.name,
            "subtitle": self.subtitle,
            "category": self.category,
            "url": self.url
        }


class ExtMaterialPreview(ExtMaterialBase):
    icon_id = Column(Integer, ForeignKey("icons.id"))

    icon = relationship(Icon, lazy="joined")

    def get_transferable(self):
        transferable = super().get_transferable()
        transferable["icon"] = self.icon.get_transferable()
        return transferable
