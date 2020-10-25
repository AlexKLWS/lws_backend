from typing import Optional, List
from enum import IntEnum
from pydantic import BaseModel

from lws_backend.pydantic_models.material import Material


class LocationType(IntEnum):
    MISC = 0
    BAR = 1
    RESTAURANT = 2
    CAFE = 3


class LocationCoords(BaseModel):
    lat: float
    lng: float


class GuideLocationInfo(BaseModel):
    referenceId: Optional[str] = None
    createdAt: Optional[str] = None
    type: LocationType
    coordinates: LocationCoords
    address: str
    title: str
    description: str
    imageUrl: str


class Guide(Material):
    defaultZoom: int
    defaultCenter: LocationCoords
    locations: List[GuideLocationInfo]
