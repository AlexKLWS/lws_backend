from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lws_backend.database_models.base import DatabaseBaseModel


class ExtMaterialBase(DatabaseBaseModel):
    __tablename__ = "ext_materials"

    reference_id = Column(String, nullable=False)
    name = Column(String)
    subtitle = Column(String)
    category = Column(Integer, default=0)


class ExtMaterialPreview(ExtMaterialBase):
    icon_id = Column(Integer, ForeignKey("icons.id"))
    url = Column(String)

    icon = relationship("Icon", lazy="joined")
