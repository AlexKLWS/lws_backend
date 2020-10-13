from sqlalchemy import Column, String

from lws_backend.database_models.base import DatabaseBaseModel
from lws_backend.pydantic_models.icon import Icon as IconJsonified


class Icon(DatabaseBaseModel):
    __tablename__ = "icons"

    data = Column(String)
    height = Column(String)
    width = Column(String)

    def get_jsonified_dict(self):
        return {
            "data": self.data,
            "height": self.height,
            "width": self.width
        }

    def from_jsonified_dict(self, i: IconJsonified):
        self.data = i.data
        if i.height is not None:
            self.height = i.height
        if i.width is not None:
            self.width = i.width
        return self
