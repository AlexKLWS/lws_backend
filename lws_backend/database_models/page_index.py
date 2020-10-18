from sqlalchemy import Column, Integer, DateTime
from lws_backend.pydantic_models.page_index import PageIndex as PageIndexJsonified

from lws_backend.database_models.base import DatabaseBaseModel


class PageIndex(DatabaseBaseModel):
    __tablename__ = "page_index"

    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    page = Column(Integer)
    category = Column(Integer, default=0)

    def get_jsonified_dict(self):
        return {
            "createdAt": self.created_at,
            "startDate": self.start_date,
            "endDate": self.end_date,
            "page": self.page,
            "category": self.category,
        }

    def from_jsonified_dict(self, p: PageIndexJsonified):
        self.created_at = p.createdAt
        self.start_date = p.startDate
        self.end_date = p.endDate
        self.category = p.category
        return self
