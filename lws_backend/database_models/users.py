from sqlalchemy import Column, String

from lws_backend.database_models.base import DatabaseBaseModel


class User(DatabaseBaseModel):
    __tablename__ = "users"

    username = Column(String)
    password = Column(String)
