from sqlalchemy import Column, String, Integer, JSON, ForeignKey

from lws_backend.database_models.base import DatabaseBaseModel
from lws_backend.pydantic_models.guide import GuideLocationInfo as GuideLocationInfoJsonified


class GuideLocationInfo(DatabaseBaseModel):
    __tablename__ = "locations"

    guide_id = Column(Integer, ForeignKey('guides.id'))
    reference_id = Column(String)
    type = Column(Integer, default=0)
    coordinates = Column(JSON)
    address = Column(String)
    title = Column(String)
    description = Column(String)
    image_url = Column(String)

    def get_jsonified_dict(self):
        return {
            "createdAt": self.created_at,
            "referenceId": self.reference_id,
            "type": self.type,
            "coordinates": self.coordinates,
            "address": self.address,
            "title": self.title,
            "description": self.description,
            "imageUrl": self.image_url,
        }

    def from_jsonified_dict(self, location: GuideLocationInfoJsonified):
        self.reference_id = location.referenceId
        self.type = location.type
        self.coordinates = location.coordinates.get_jsonified_dict()
        self.address = location.address
        self.title = location.title
        self.description = location.description
        self.image_url = location.imageUrl
        if location.createdAt is not None:
            self.created_at = location.createdAt
        return self
