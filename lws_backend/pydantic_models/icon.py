from typing import Optional
from pydantic import BaseModel


class Icon(BaseModel):
    data: str
    width: Optional[str] = None
    height: Optional[str] = None
