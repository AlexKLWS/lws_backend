from sqlalchemy import Column, String, Integer

from lws_backend.database_models.base import DatabaseBaseModel


class User(DatabaseBaseModel):
    __tablename__ = "users"

    username = Column(String)
    password = Column(String)
    access = Column(Integer, default=0)
