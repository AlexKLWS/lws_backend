from typing import Optional, List
from enum import IntEnum
from pydantic import BaseModel
from datetime import datetime

from lws_backend.pydantic_models.material import Material
from lws_backend.pydantic_models.icon import Icon


class LocationType(IntEnum):
    MISC = 0
    BAR = 1
    RESTAURANT = 2
    CAFE = 3


class LocationCoords(BaseModel):
    lat: float
    lng: float

    def get_jsonified_dict(self):
        return {
            "lat": self.lat,
            "lng": self.lng
        }


class GuideLocationInfo(BaseModel):
    referenceId: Optional[str] = None
    createdAt: Optional[datetime] = None
    type: LocationType
    coordinates: LocationCoords
    address: str
    title: str
    description: str
    imageUrl: str


class GuidePreview(Material):
    icon: Icon


class Guide(GuidePreview):
    info: str
    defaultZoom: int
    defaultCenter: LocationCoords
    locations: List[GuideLocationInfo]
