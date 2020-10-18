from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from lws_backend.pydantic_models.category import Category


class PageIndex(BaseModel):
    createdAt: Optional[datetime] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    page: int
    category: Category
