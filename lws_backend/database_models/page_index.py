from sqlalchemy import Column, Integer, String, DateTime

from lws_backend.database_models.base import DatabaseBaseModel


class PageIndex(DatabaseBaseModel):
    __tablename__ = "page_index"

    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    page = Column(Integer)
    category = Column(Integer, default=0)
