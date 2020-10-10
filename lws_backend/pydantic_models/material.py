from pydantic import BaseModel
from datetime import datetime

from lws_backend.pydantic_models.category import Category


class Material(BaseModel):
    createdAt: datetime
    referenceId: str
    name: str
    subtitle: str
    category: Category
