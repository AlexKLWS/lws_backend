from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from lws_backend.pydantic_models.category import Category


class Material(BaseModel):
    createdAt: Optional[datetime] = None
    referenceId: Optional[str] = None
    name: str
    subtitle: str
    category: Category
