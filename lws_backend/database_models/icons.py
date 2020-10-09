from sqlalchemy import Column, String

from lws_backend.database_models.base import DatabaseBaseModel


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
