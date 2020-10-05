from sqlalchemy import Column, String

from lws_backend.database_models.base import DatabaseBaseModel


class Icon(DatabaseBaseModel):
    __tablename__ = "icons"

    data = Column(String)
    height = Column(String)
    width = Column(String)
